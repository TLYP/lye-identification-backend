import deezer.client
from flask import Flask, jsonify, request
from shazamio import Shazam, Serialize
import base64
import json
import deezer

app = Flask(__name__)


@app.route("/", methods=["get"])
async def hello_world():
    data = {"hello": "world"}
    return jsonify(data)


@app.route("/identify", methods=["POST"])
async def identify():
    shazam = Shazam()
    data = request.data

    byte = base64.b64decode(data)

    info = await shazam.recognize_song(byte)

    for match in info["matches"]:
        track_data = await shazam.track_about(match["id"])
        track = Serialize.track(track_data)

        print(track.title)

    with open("data.json", "w") as f:
        json.dump(info, f, indent=4)

    # with deezer.Client() as client:
    #     result = client.search(track=info["track"]["title"], artist="Mili")
    #     if len(result) == 0:
    #         return jsonify({"code": "1", "message": "song not found"})

    #     for track in result:
    #         print(json.dumps(track.as_dict(), indent=4))

    #     # track: deezer.Track = result[0]
    #     # print(json.dumps(track.as_dict(), indent=4))

    #     # print(json.dumps(result, indent=4))

    # with open("data.json", "w") as f:
    #     json.dump(info, f, indent=4)

    data = {"hello": "world"}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
