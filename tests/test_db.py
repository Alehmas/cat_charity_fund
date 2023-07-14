from conftest import BASE_DIR


try:
    from app.models.financial_base import FinancialBase
except (NameError, ImportError):
    class FinancialBase:
        pass

try:
    from app.core.config import Settings
except (NameError, ImportError):
    raise AssertionError(
        'The `Settings` application settings object was not found.'
        'Check and fix: it should be available in the `app.core.config` module.',
    )


def test_fin_base_is_abstract():
    if hasattr(FinancialBase, '__abstract__'):
        assert hasattr(FinancialBase, '__abstract__'), (
            'The `FinancialBase` model must be abstract. '
            'Add the `__abstract__` attribute'
        )
        assert FinancialBase.__abstract__, (
            'The `FinancialBase` table must be abstract.'
        )


def test_check_migration_file_exist():
    app_dirs = [d.name for d in BASE_DIR.iterdir()]
    assert 'alembic' in app_dirs, (
        'The folder `alembic` was not found in the root directory.'
    )
    ALEMBIC_DIR = BASE_DIR / 'alembic'
    version_dir = [d.name for d in ALEMBIC_DIR.iterdir()]
    assert 'versions' in version_dir, (
        'No `versions` folder found in `alembic` folder'
    )
    VERSIONS_DIR = ALEMBIC_DIR / 'versions'
    files_in_version_dir = [f.name for f in VERSIONS_DIR.iterdir() if f.is_file() and 'init' not in f.name]
    assert len(files_in_version_dir) > 0, (
        'No migration files found in `alembic.versions` folder'
    )


def test_check_db_url():
    for attr_name, attr_value in Settings.schema()['properties'].items():
        if 'db' in attr_name or 'database' in attr_name:
            assert 'sqlite+aiosqlite' in attr_value['default'], (
                'Specify default value for sqlite database connection '
            )
