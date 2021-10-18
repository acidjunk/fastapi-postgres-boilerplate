from unittest import mock

import pytest
from sqlalchemy.orm.exc import NoResultFound

from server.db import ProductsTable, db, transactional
from server.utils.date_utils import nowtz


def test_transactional():
    def insert_p(state):
        p = ProductsTable(
            name="Test transactional",
            description="Testing 1, 2, 3!",
            created_at=nowtz(),
        )
        db.session.add(p)

    def insert_p_error(state):
        p = ProductsTable(
            name="Test transactional [ERROR]",
            description="Testing 1, 2, 3! BOOM!",
            created_at=nowtz(),
        )
        db.session.add(p)
        raise Exception("Let's wreck some havoc!")

    logger = mock.MagicMock()

    with transactional(db, logger):
        insert_p({})
    logger.assert_has_calls(
        [
            mock.call.debug("Temporarily disabling commit."),
            mock.call.debug("Reenabling commit."),
            mock.call.debug("Committing transaction."),
        ]
    )

    logger.reset_mock()
    with pytest.raises(Exception):
        with transactional(db, logger):
            insert_p_error({})

    logger.assert_has_calls(
        [
            mock.call.debug("Temporarily disabling commit."),
            mock.call.debug("Reenabling commit."),
            mock.call.warning("Rolling back transaction."),
        ]
    )


def test_transactional_no_commit():
    def insert_p(state):
        p = ProductsTable(
            name="Test transactional should not be committed",
            description="Testing 1, 2, 3!",
            created_at=nowtz(),
        )
        db.session.add(p)
        db.session.commit()

        raise Exception("Lets rollback")

    logger = mock.MagicMock()

    with pytest.raises(Exception, match="Lets rollback"):
        with transactional(db, logger):
            insert_p({})

    assert (
        db.session.query(ProductsTable).filter(ProductsTable.name == "Test transactional should not be committed").all()
        == []
    )
    logger.assert_has_calls(
        [
            mock.call.warning(
                "Step function tried to issue a commit. It should not! Will execute commit on behalf of step function when it returns."
            ),
        ]
    )


def test_transactional_no_commit_second_thread():
    def insert_p(state):
        p = ProductsTable(
            name="Test transactional should not be committed",
            description="Testing 1, 2, 3!",
            created_at=nowtz(),
        )
        db.session.add(p)
        db.session.commit()

        # Create new database session to simulate another workflow/api handler running at the same time
        # This is also a workaround for our disable commit wrapper but it should be reasonable obvious that
        # someone is fucking around if you see `with db.database_scope():` in actual production code

        with db.database_scope():
            p2 = ProductsTable(
                name="Test transactional should be committed",
                description="Testing 1, 2, 3!",
                created_at=nowtz(),
            )
            db.session.add(p2)
            db.session.commit()

        raise Exception("Lets rollback")

    logger = mock.MagicMock()

    with pytest.raises(Exception, match="Lets rollback"):
        with transactional(db, logger):
            insert_p({})

    assert db.session.query(ProductsTable).filter(ProductsTable.name == "Test transactional should be committed").one()
    assert (
        db.session.query(ProductsTable).filter(ProductsTable.name == "Test transactional should not be committed").all()
        == []
    )
    logger.assert_has_calls(
        [
            mock.call.warning(
                "Step function tried to issue a commit. It should not! Will execute commit on behalf of step function when it returns."
            ),
        ]
    )


def test_autouse_fixture_rolls_back_aaa():
    # We want to test whether a change committed to the database in one test is visible to other tests (as in really
    # persisted to the database). Of course such a change should not be visible if our `flask_app` and `database`
    # autouse fixtures work as advertised.
    #
    # However, tests should be independent of each other and we cannot assume one test runs before the other. Hence
    # this test comes in two versions: one with the `_aaa` postfix and one with the `_bbb` postfix. Both will test
    # for the presence of a change the other test thinks it has committed to the database. If one of the tests (the
    # one that runs after the other) finds the change the other has committed our fixtures don't work properly.

    # Using Products as it's a simple model that doesn't require foreign keys.
    p = ProductsTable(name="aaa", description="aaa", created_at=nowtz())

    db.session.add(p)
    db.session.commit()

    with pytest.raises(NoResultFound):
        ProductsTable.query.filter(ProductsTable.name == "bbb").one()


def test_autouse_fixture_rolls_back_bbb():
    # We want to test whether a change committed to the database in one test is visible to other tests (as in really
    # persisted to the database). Of course such a change should not be visible if our `flask_app` and `database`
    # autouse fixtures work as advertised.
    #
    # However, tests should be independent of each other and we cannot assume one test runs before the other. Hence
    # this test comes in two versions: one with the `_aaa` postfix and one with the `_bbb` postfix. Both will test
    # for the presence of a change the other test thinks it has committed to the database. If one of the tests (the
    # one that runs after the other) finds the change the other has committed our fixtures don't work properly.

    # Using ResourceTypeTable as it's a simple model than doesn't require foreign keys.
    p = ProductsTable(name="bbb", description="bbb", created_at=nowtz())
    db.session.add(p)
    db.session.commit()

    with pytest.raises(NoResultFound):
        ProductsTable.query.filter(ProductsTable.name == "aaa").one()


def test_str_method():
    assert str(ProductsTable()) == "ProductsTable(id=None, name=None, description=None, created_at=None)"
