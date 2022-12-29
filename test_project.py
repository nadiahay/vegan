# ----------------------------------------------------------------------------#
# This file contains the tests for the project
# Run with: $ pytest
# ----------------------------------------------------------------------------#


import app
import pytest
import os
import sha3


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
        "date": "2022-12-29",
        "contentHash": "5d33a5c6d7c9149fc2a40603c1f1a249d0add248e1ad77edb08e0832905cfd92",
    }

def test_get_all_blog_content():
    # Test that the get_all_blog_content function returns the correct
    # list of blog posts
    posts = app.get_all_blog_content()

    assert len(posts) > 1


def test_hashing():
    # Test that the hashing function works correctly
    # Ref: sha3.keccak_256(content_md.encode("utf-8")).hexdigest()
    string  = "test test test"
    assert sha3.keccak_256(string.encode("utf-8")).hexdigest() == "5d33a5c6d7c9149fc2a40603c1f1a249d0add248e1ad77edb08e0832905cfd92"
    assert sha3.keccak_256(string.encode("utf-8")).hexdigest() != "5d33a5c6d7c9149fc2a40603c1f1a249d0add248e1ad77edb08e0832905cfd93"
    assert sha3.keccak_256(string.encode("utf-8")).hexdigest() != "hello world"