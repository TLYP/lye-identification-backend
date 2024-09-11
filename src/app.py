from flask import Flask, jsonify, request
from shazamio import Shazam
import base64
import json
from spotify_utils import EnhancedJSONEncoder, spotify_search


app = Flask(__name__)


@app.route("/", methods=["get"])
async def hello_world():
    data = {"hello": "world"}
    return jsonify(data)


@app.route("/spotify_search", methods=["GET"])
async def spotify_meta():
    query = request.args.get("q")

    if not query:
        return jsonify({"code": 1})

    songs = spotify_search(query)

    data = {
        "code": 0,
        "query": query,
        "tracks": json.loads(json.dumps(songs, indent=4, cls=EnhancedJSONEncoder)),
    }

    return jsonify(data)


@app.route("/identify", methods=["POST"])
async def identify():
    shazam = Shazam()
    data = request.data

    byte = base64.b64decode(data)

    try:
        info = await shazam.recognize_song(byte)
    except Exception as e:
        print("error while recognize", e, ";")
        return jsonify({"code": 1})

    title = info["track"]["title"]

    songs = spotify_search(title)

    data = {
        "code": 0,
        "query": title,
        "tracks": json.loads(json.dumps(songs, indent=4, cls=EnhancedJSONEncoder)),
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
