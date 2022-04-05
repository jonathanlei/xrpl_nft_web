import React, { Component } from "react";
import Clock from "../components/Clock";
import Footer from '../components/footer';

export default class Createpage extends Component {

constructor() {
    super();
    this.onChange = this.onChange.bind(this);
    this.state = {
      files: null,
      title: "", 
      description: "",
      price: "",
      preiewUrl: "", 
    };
  }

  onChange(evt) {
    evt.preventDefault();
    const {name, value} = evt.target;
    if (name === "files"){
      console.log("HERE");
      document.getElementById("file_name").style.display = "none";
      let url = window.webkitURL.createObjectURL(value);
      console.log(url);
      this.setState(fData => ({...fData, preiewUrl:url}));
    }
    this.setState(fData =>  ({...fData, [name]: value}));
  }


  

render() {
    return (
      <div>

        <section className='jumbotron breadcumb no-bg'>
          <div className='mainbreadcumb'>
            <div className='container'>
              <div className='row m-10-hor'>
                <div className='col-12'>
                  <h1 className='text-center'>Create</h1>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className='container'>

        <div className="row">
          <div className="col-lg-7 offset-lg-1 mb-5">
              <form id="form-create-item" className="form-border" action="#">
                  <div className="field-set">
                      <h5>Upload file</h5>

                      <div className="d-create-file">
                          {this.state.files ? <></> : <p id="file_name">PNG, JPG, GIF, WEBP or MP4. Max 200mb.</p> }
                        { this.state.files ?  (<p key="{index}">{this.state.files}</p>) : <></>}
                        
                          <div className='browse'>
                            <input type="button" id="get_file" className="btn-main" value="Browse"/>
                            <input name="files" id='upload_file' type="file" onChange={this.onChange} />
                          </div>
                          
                      </div>

                      <div className="spacer-single"></div>

                      <h5>Title</h5>
                      <input type="text" name="item_title" id="item_title" className="form-control" placeholder="e.g. 'Crypto Funk"  onChange={this.onChange} />

                      <div className="spacer-10"></div>

                      <h5>Description</h5>
                      <textarea data-autoresize name="item_desc" id="item_desc" className="form-control" placeholder="e.g. 'This is very limited item'" value={this.state.description} onChange={this.onChange} ></textarea>

                      <div className="spacer-10"></div>

                      <h5>Price</h5>
                      <input type="text" name="item_price" id="item_price" className="form-control" placeholder="enter price for one item (XRP)"  value={this.state.value} onChange={this.onChange} />

                      <div className="spacer-10"></div>
                      <div className="spacer-10"></div>

                      <input type="button" id="submit" className="btn-main" value="Create Item"/>
                  </div>
              </form>
          </div>

          <div className="col-lg-3 col-sm-6 col-xs-12">
                  <h5>Preview item</h5>
                  <div className="nft__item m-0">
                      <div className="de_countdown">
                        <Clock deadline="December, 30, 2021" />
                      </div>
                      <div className="author_list_pp">
                          <span>                                    
                              <img className="lazy" src="./img/author/author-1.jpg" alt=""/>
                              <i className="fa fa-check"></i>
                          </span>
                      </div>
                      <div className="nft__item_wrap">
                          <span>
                              <img src={this.state.previewUrl} id="get_file_2" className="lazy nft__item_preview" alt=""/>
                          </span>
                      </div>
                      <div className="nft__item_info">
                          <span >
                              <h4>{this.state.title}</h4>
                          </span>
                          <div className="nft__item_price">
                              {this.state.price}XRP<span>{this.state.price}</span>
                          </div>
                          <div className="nft__item_action">
                              <span>Place a bid</span>
                          </div>
                          <div className="nft__item_like">
                              <i className="fa fa-heart"></i><span>50</span>
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
}