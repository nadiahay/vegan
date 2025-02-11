# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request
import json
import os
import hashlib
import re
import markdown
import datetime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
# set static and template folders
app.template_folder = "frontend/html"
app.static_folder = "frontend/assets"


# ----------------------------------------------------------------------------#
# Routes.
# ----------------------------------------------------------------------------#


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog2")
def blog2():
    return render_template("blog.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/donate")
def donate():
    return render_template("donate.html")


@app.route("/post")
def post():
    return render_template("post.html")


# ----------------------------------------------------------------------------#
# Blog
# ----------------------------------------------------------------------------#


@app.route("/blog/<post>", methods=["GET"])
def blog_post(post):
    base_path = app.template_folder + "/blog/" + post + "/"
    try:
        post_html, details = get_blog_post(base_path, post)
    except FileNotFoundError:
        return "404: Don't mess around with the url pls :)", 404

    # render the post
    return render_template(
        "blog/blogpost.html",
        post=post,
        post_html=post_html,
        details=details,
    )


@app.route("/blog", methods=["GET"])
def blog():
    # get all blog posts and their preview content
    posts = get_all_blog_content()
    return render_template("/blog/blog.html", posts=posts)


def get_all_blog_content():
    posts = []
    for post in os.listdir(app.template_folder + "/blog/"):
        # skip if not a directory
        if not os.path.isdir(app.template_folder + "/blog/" + post):
            continue

        # call blog_post() to generate content_preview.html file
        if not os.path.exists(
            app.template_folder + "/blog/" + post + "/content_preview.html"
        ) or not os.path.exists(
            app.template_folder + "/blog/" + post + "/details.json"
        ):
            # generate content_preview.html file (and everything else)
            get_blog_post(app.template_folder + "/blog/" + post + "/", post)

        with open(app.template_folder + "/blog/" + post + "/details.json") as f:
            details = json.load(f)

        if details["isPublished"] == "true":
            posts.append(
                {
                    "slug": details["slug"],
                    "author": details["author"],
                    "tags": details["tags"],
                    "date": details["date"],
                    "content_preview": open(
                        app.template_folder + "/blog/" + post + "/content_preview.html"
                    ).read(),
                    "post": post,
                }
            )

    # sort posts by date
    posts = sorted(posts, key=lambda k: k["date"], reverse=True)
    return posts


def get_blog_post(post_path, post):
    # load details.json file if it exists, else use default values & save to file
    if os.path.exists(post_path + "details.json"):
        with open(post_path + "details.json") as f:
            details = json.load(f)
        print(f"DETAILS: {details}")
    else:
        today = datetime.datetime.now()
        details = {
            "slug": post,
            "author": "Nadia Hayajneh",
            "tags": "",
            "isPublished": "true",
            "overwriteHtml": "true",
            "date": today.strftime("%Y-%m-%d"),
            "contentHash": "",
        }
        # save details.json file
        with open(post_path + "details.json", "w") as f:
            json.dump(details, f, indent=4)

    # CHECK IF THE CONTENT HAS CHANGED
    content_md = open(post_path + "content.md", "r").read()
    content_hash = hashlib.sha3_256(content_md.encode("utf-8")).hexdigest()
    rerender_flag = False
    # compare to existing hash in details.json
    if details["contentHash"] != content_hash:
        details["contentHash"] = content_hash
        with open(post_path + "details.json", "w") as f:
            json.dump(details, f, indent=4)
        rerender_flag = True and details["overwriteHtml"]

    if not os.path.exists(post_path + "content.html") or rerender_flag:
        # takes in blog/<post>/content.md, turns it into html and renders it
        post_html = markdown.markdown(open(post_path + "content.md").read())

        # DO NOT TOUCHHHHH
        # replace all internal links so they point to the correct place
        pattern = re.compile(r'src="(?!(https://|http://))([^"]*)"')
        post_html = pattern.sub(r'src="../src/html/blog/' + post + r'/\2"', post_html)

        # save html to file
        with open(post_path + "content.html", "w") as f:
            f.write(post_html)
    else:
        post_html = open(post_path + "content.html").read()

    if not os.path.exists(post_path + "content_preview.html") or rerender_flag:
        post_html = open(post_path + "content.html").read()
        # if no '<img ' in content_preview, add next paragraph until there is one

        p_counter = 0
        content_preview = post_html.split("</p>")[p_counter] + "</p>"
        if "<img " in post_html:
            while "<img " not in content_preview:
                p_counter += 1
                if p_counter > 4:  # max 4 paragraphs
                    break
                content_preview += post_html.split("</p>")[p_counter] + "</p>"

        print(f"CONTENT PREVIEW: {content_preview}")
        # save content_preview.html file
        with open(post_path + "content_preview.html", "w") as f:
            f.write(content_preview)

    return post_html, details


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#


def main():
    # generate all blog posts
    get_all_blog_content()

    app.config.update(
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True,
    )
    app.run()


# Default port:
if __name__ == "__main__":
    main()
