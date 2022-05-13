import React, { useState, useContext } from "react";
import Clock from "../components/Clock";
import Footer from "../components/footer";
import frontendAPI from "../../core/axios";
import UserContext from "../../usercontext";

const initialForm = {
  image: "",
  title: "",
  description: "",
  price: "",
  previewUrl: "",
};
/* TODO: create current user object and check if authorized to do this */
function CreatePage() {
  let currentUser = useContext(UserContext);
  let [formData, setFormData] = useState(initialForm);
  function handleChange(evt) {
    const { name, value } = evt.target;
    if (name === "image") {
      let url = URL.createObjectURL(evt.target.files[0]);
      setFormData((fData) => ({
        ...fData,
        image: evt.target.files[0],
        previewUrl: url,
      }));
    }
    setFormData((fData) => ({ ...fData, [name]: value }));
  }

  async function handleSubmit(evt) {
    evt.preventDefault();
    let res = await frontendAPI.mintNFT({
      ...formData,
      owner: currentUser,
    });
    console.log(res, "HERE");
  }
  return (
    <div>
      <section className="jumbotron breadcumb no-bg">
        <div className="mainbreadcumb">
          <div className="container">
            <div className="row m-10-hor">
              <div className="col-12">
                <h1 className="text-center">Create</h1>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="container">
        <div className="row">
          <div className="col-lg-7 offset-lg-1 mb-5">
            <form id="form-create-item" className="form-border" action="#">
              <div className="field-set">
                <h5>Upload file</h5>

                <div className="d-create-file">
                  {formData.image ? (
                    <></>
                  ) : (
                    <p id="file_name">PNG, JPG, GIF, WEBP or MP4. Max 200mb.</p>
                  )}
                  {formData.image ? (
                    <p key="{index}">{formData.image}</p>
                  ) : (
                    <></>
                  )}

                  <div className="browse">
                    <input
                      type="button"
                      id="get_file"
                      className="btn-main"
                      value="Browse"
                      name="get_file"
                      onChange={handleChange}
                    />
                    <input
                      name="image"
                      id="upload_file"
                      type="file"
                      onChange={handleChange}
                    />
                  </div>
                </div>

                <div className="spacer-single"></div>

                <h5>Title</h5>
                <input
                  type="text"
                  name="title"
                  id="title"
                  className="form-control"
                  placeholder="e.g. 'Crypto Funk"
                  value={formData.title}
                  onChange={handleChange}
                />

                <div className="spacer-10"></div>

                <h5>Description</h5>
                <textarea
                  data-autoresize
                  name="description"
                  id="description"
                  className="form-control"
                  placeholder="e.g. 'This is very limited item'"
                  value={formData.description}
                  onChange={handleChange}
                ></textarea>

                <div className="spacer-10"></div>

                <h5>Price</h5>
                <input
                  name="price"
                  type="number"
                  min="1"
                  step="1"
                  id="price"
                  className="form-control"
                  placeholder="enter price for one item (XRP)"
                  value={formData.price}
                  onChange={handleChange}
                />

                <div className="spacer-10"></div>
                <div className="spacer-10"></div>
                <h6>
                  Your NFT will be uploaded to IPFS and minted on the XRP ledger
                  once you approve the transaction
                </h6>
                <div className="spacer-10"></div>
                <div className="spacer-10"></div>
                <input
                  type="button"
                  id="submit"
                  className="btn-main"
                  value="Create Item"
                  onClick={handleSubmit}
                />
              </div>
            </form>
          </div>

          <div className="col-lg-3 col-sm-6 col-xs-12">
            <h5>Preview item</h5>
            <div className="nft__item m-0">
              <div className="author_list_pp">
                <span>
                  <img
                    className="lazy"
                    src="./img/author/author-1.jpg"
                    alt=""
                  />
                  <i className="fa fa-check"></i>
                </span>
              </div>
              <div className="nft__item_wrap">
                <span>
                  <img
                    src={formData.previewUrl}
                    id="get_file_2"
                    className="lazy nft__item_preview"
                    alt=""
                  />
                </span>
              </div>
              <div className="nft__item_info">
                <span>
                  <h4>{formData.title}</h4>
                </span>
                <div className="nft__item_price">{formData.price} XRP</div>
                <div className="nft__item_action">
                  <span>Place a bid</span>
                </div>
                <div className="nft__item_like">
                  <i className="fa fa-heart"></i>
                  <span>50</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default CreatePage;
