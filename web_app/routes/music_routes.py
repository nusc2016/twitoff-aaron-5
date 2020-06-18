from flask import Blueprint, jsonify, request, render_template
# flash, direct

from web_app.models import Music, db, parse_records

music_routes = Blueprint("music_routes", __name__)


def list_music():
    # music = [
    #     {"id": 1, "title": "Music 1"},
    #     {"id": 2, "title": "Music 2"},
    #     {"id": 3, "title": "Music 3"},
    # ]
    music_records = Music.query.all()
    print(music_records)
    books = parse_records(music_records)
    return jsonify(music)

# SELECT * FROM music


@music_routes.route("/music")
def list_music_for_humans():
    # books = [
    #     {"id": 1, "title": "Music 1"},
    #     {"id": 2, "title": "Music 2"},
    #     {"id": 3, "title": "Music 3"},
    # ]
    music_records = Music.query.all()
    print(music_records)
    books = parse_records(music_records)  # optionally
    return render_template("music.html", message="Here's some music",
                           music=music)


@music_routes.route("/music/new")
def new_music():
    return render_template("new_music.html")

# INSERT INTO music ...


@music_routes.route("/music/create", methods=["POST"])
def create_music():
    print("FORM DATA:", dict(request.form))

    new_music = Music(album_title=request.form["album_title"],
                      artist_id=request.form["artist_name"])
    db.session.add(new_music)
    db.session.commit()

    return jsonify({
        "message": "MUSIC CREATED OK",
        "music": dict(request.form)
    })
    # flash(f"Music '{new_music.title}' created successfully!",
    # "success")
    # return redirect(f"/music)
