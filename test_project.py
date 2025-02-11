# ----------------------------------------------------------------------------#
# This file contains the tests for the project
# Run with: $ pytest
# ----------------------------------------------------------------------------#


import app
# import pytest
import os
import hashlib


def test_get_blog_post():
    # Test that the get_blog_post function returns the correct html
    # and details for a given blog post
    base_path = app.app.template_folder + "/blog/" + "test" + "/"

    # delete all files in the test directory except content.md
    for file in os.listdir(base_path):
        if file != "content.md":
            os.remove(base_path + file)

    # generate all files
    post_html, details = app.get_blog_post(base_path, "test")

    assert post_html == "<p>test test test</p>"
    assert details == {
        "slug": "test",
        "author": "Nadia Hayajneh",
        "tags": "",
        "isPublished": "true",
        "overwriteHtml": "true",
        "date": "2025-02-11",
        "contentHash": "e47deee8079b206ced5815beee15fb89a8d8c17aca4aa24b3eeac2acb169e7df",
    }


def test_get_all_blog_content():
    # Test that the get_all_blog_content function returns the correct
    # list of blog posts
    posts = app.get_all_blog_content()

    assert len(posts) > 1


def test_hashing():
    # Test that the hashing function works correctly
    string = "test test test"
    expected_hash = "e47deee8079b206ced5815beee15fb89a8d8c17aca4aa24b3eeac2acb169e7df"
    assert hashlib.sha3_256(string.encode("utf-8")).hexdigest() == expected_hash
    assert hashlib.sha3_256(string.encode("utf-8")).hexdigest() != "hello world"
