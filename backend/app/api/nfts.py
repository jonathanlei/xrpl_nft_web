from flask import Blueprint, jsonify, session, request, Response
from flask_login import login_required, current_user
from models import User, Nft, Transaction, Auction, db
from aws import upload_file_to_s3, allowed_file, get_unique_filename
from nft_transactions.ipfs import upload_to_ipfs
from nft_transactions.xrp_transact import mintNft
from flask_cors import CORS, cross_origin
nft_routes = Blueprint("nfts", __name__)

""" TODO: add wallet intergration and add wallet route """


@nft_routes.route("/")
def nfts():
    nfts = Nft.query.all()
    return {"nfts": [nfts.to_dict() for nft in nfts]}


@nft_routes.route("/<int:id>")
def nft(id):
    nft = Nft.query.get(id)
    return {"nft": nft.to_dict()}


@nft_routes.route("/mint/", methods=["POST"])
def mint():
    data = request.json
    # upload to aws
    if "image" not in request.files:
        return {"errors": "image required"}, 400

    image = request.files["image"]
    if not allowed_file(image.filename):
        return {"errors": "file type not permitted"}, 400

    image.filename = get_unique_filename(image.filename)
    data["url"] = upload_file_to_s3(image)["url"]

    # upload to ipfs
    uri = upload_to_ipfs(image)
    # add uri and contract id.
    print("GETTING TO MINT NFT FUNCTION CALL")
    # return {"msg": "received"}
    return mintNft(data["owner"], uri, data)


@nft_routes.route("<int:id>/update/", methods=["PUT"])
@login_required
def update_nft_meta(id):
    data = request.json
    nft = Nft.query.filter(Nft.id == id).one()
    if current_user.id != data["owner_id"]:
        return Response("not authorized", 401)
    if "title" in data:
        nft.title = data["title"]
    if "description" in data:
        nft.description = data["description"]
    db.session.commit()
    return {"nft": nft.to_dict()}


@nft_routes.route("/:id", methods=["DELETE"])
@login_required
# TODO: add on chain deletion
def delete_nft():
    nft = Nft.query.get(id)
    db.session.delete(nft)
    db.session.commit()
    return {"msg": "nft deleted successfully"}, 200


CORS(nft_routes)
