"""
    Helper to publish this Project to PyPi
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

import xnbtd


PACKAGE_ROOT = Path(xnbtd.__file__).parent.parent


def verbose_check_call(*args):
    """Run subprocess.check_call() with verbose output."""
    print(f"Call: {' '.join(repr(arg) for arg in args)}")
    return subprocess.check_call(
        args,
        universal_newlines=True,
        env=os.environ
    )


def publish(skip_upload=False, skip_tests=False, skip_lint=False):
    """
    Publish to PyPi
    Call this via:
        $ poetry run publish

    Args:
        skip_upload (bool): If True, only build the package but don't upload to PyPI
        skip_tests (bool): If True, skip running tests before publishing
        skip_lint (bool): If True, skip running linting before publishing
    """
    try:
        if not skip_tests:
            print("Running tests...")
            try:
                verbose_check_call('poetry', 'run', 'python', '-m', 'pytest')
            except subprocess.CalledProcessError:
                # Fallback to Django's test command if pytest fails
                try:
                    os.environ['DJANGO_SETTINGS_MODULE'] = 'xnbtd.settings.test'
                    verbose_check_call('poetry', 'run', 'python', 'manage.py', 'test')
                except subprocess.CalledProcessError as e:
                    print(f"Tests failed: {e}")
                    if input("Tests failed. Continue anyway? (y/N): ").lower() != 'y':
                        print("Aborting publish.")
                        return
        else:
            print("Skipping tests.")

        if not skip_lint:
            print("Running linting...")
            try:
                verbose_check_call('poetry', 'run', 'flake8', '.')
            except subprocess.CalledProcessError as e:
                print(f"Linting failed: {e}")
                if input("Linting failed. Continue anyway? (y/N): ").lower() != 'y':
                    print("Aborting publish.")
                    return
        else:
            print("Skipping linting.")

        # Build the package
        print("Building package...")
        verbose_check_call('poetry', 'build')

        if not skip_upload:
            # Ask for confirmation before uploading to PyPI
            response = input("\nDo you want to upload the package to PyPI? (y/N): ")
            if response.lower() == 'y':
                # Upload to PyPI
                try:
                    verbose_check_call('poetry', 'publish')
                    print("\n✅ Package successfully published to PyPI!")
                except subprocess.CalledProcessError as e:
                    print(f"\n❌ Failed to publish package: {e}")
                    print("\nIf you're having authentication issues, try running:")
                    print("  poetry config pypi-token.pypi YOUR_API_TOKEN")
                    print("  or")
                    print("  poetry config http-basic.pypi username password")
            else:
                print("\n⏭️ Upload to PyPI skipped.")
        else:
            print("\n⏭️ Upload to PyPI skipped (--skip-upload flag used).")

        print("\n📦 Package built successfully in the 'dist' directory.")
    except Exception as e:
        print(f"Error during publishing: {e}")
        if input("An error occurred. Continue anyway? (y/N): ").lower() != 'y':
            raise


def main():
    """Command-line interface for the publish script."""
    parser = argparse.ArgumentParser(description="Build and publish the package to PyPI")
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Skip uploading to PyPI and only build the package"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests before publishing"
    )
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip running linting before publishing"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force publishing even if tests or linting fail"
    )
    args = parser.parse_args()

    try:
        publish(
            skip_upload=args.skip_upload,
            skip_tests=args.skip_tests,
            skip_lint=args.skip_lint
        )
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
