import React from 'react';
import Footer from '../components/footer';
import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  header#myHeader.navbar.sticky.white {
    background: #403f83;
    border-bottom: solid 1px #403f83;
  }
  header#myHeader.navbar .search #quick_search{
    color: #fff;
    background: rgba(255, 255, 255, .1);
  }
  header#myHeader.navbar.white .btn, .navbar.white a, .navbar.sticky.white a{
    color: #fff;
  }
  header#myHeader .dropdown-toggle::after{
    color: rgba(255, 255, 255, .5);
  }
  header#myHeader .logo .d-block{
    display: none !important;
  }
  header#myHeader .logo .d-none{
    display: block !important;
  }
  @media only screen and (max-width: 1199px) {
    .navbar{
      background: #403f83;
    }
    .navbar .menu-line, .navbar .menu-line1, .navbar .menu-line2{
      background: #fff;
    }
    .item-dropdown .dropdown a{
      color: #fff !important;
    }
  }
`;

const news= () => (
<div>
<GlobalStyles/>

  <section className='jumbotron breadcumb no-bg' style={{backgroundImage: `url(${'./img/background/subheader.jpg'})`}}>
    <div className='mainbreadcumb'>
      <div className='container'>
        <div className='row m-10-hor'>
          <div className='col-12 text-center'>
            <h1>News</h1>
            <p>Anim pariatur cliche reprehenderit</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section className='container'>
    <div className="row">
      <div className="col-lg-4 col-md-6 mb30">
        <div className="bloglist item">
            <div className="post-content">
                <div className="post-image">
                    <img alt="" src="./img/news/news-1.jpg" className="lazy"/>
                </div>
                <div className="post-text">
                    <span className="p-tagline">Tips &amp; Tricks</span>
                    <span className="p-date">October 28, 2020</span>
                    <h4><span>The next big trend in crypto<span></span></span></h4>
                    <p>Dolore officia sint incididunt non excepteur ea mollit commodo ut enim reprehenderit cupidatat labore ad laborum consectetur consequat...</p>
                    <span className="btn-main">Read more</span>
                </div>
            </div>
        </div>
      </div>
      
      <div className="col-lg-4 col-md-6 mb30">
        <div className="bloglist item">
            <div className="post-content">
                <div className="post-image">
                    <img alt="" src="./img/news/news-2.jpg" className="lazy"/>
                </div>
                <div className="post-text">
                    <span className="p-tagline">Tips &amp; Tricks</span>
                    <span className="p-date">October 28, 2020</span>
                    <h4><span>The next big trend in crypto<span></span></span></h4>
                    <p>Dolore officia sint incididunt non excepteur ea mollit commodo ut enim reprehenderit cupidatat labore ad laborum consectetur consequat...</p>
                    <span className="btn-main">Read more</span>
                </div>
            </div>
        </div>
      </div>
      
      <div className="col-lg-4 col-md-6 mb30">
        <div className="bloglist item">
            <div className="post-content">
                <div className="post-image">
                    <img alt="" src="./img/news/news-3.jpg" className="lazy"/>
                </div>
                <div className="post-text">
                    <span className="p-tagline">Tips &amp; Tricks</span>
                    <span className="p-date">October 28, 2020</span>
                    <h4><span>The next big trend in crypto<span></span></span></h4>
                    <p>Dolore officia sint incididunt non excepteur ea mollit commodo ut enim reprehenderit cupidatat labore ad laborum consectetur consequat...</p>
                    <span className="btn-main">Read more</span>
                </div>
            </div>
        </div>
      </div>
      
      <div className="col-lg-4 col-md-6 mb30">
        <div className="bloglist item">
                <div className="post-content">
                    <div className="post-image">
                        <img alt="" src="./img/news/news-4.jpg" className="lazy"/>
                    </div>
                    <div className="post-text">
                        <span className="p-tagline">Tips &amp; Tricks</span>
                        <span className="p-date">October 28, 2020</span>
                        <h4><span>The next big trend in crypto<span></span></span></h4>
                        <p>Dolore officia sint incididunt non excepteur ea mollit commodo ut enim reprehenderit cupidatat labore ad laborum consectetur consequat...</p>
                        <span className="btn-main">Read more</span>
                    </div>
                </div>
            </div>
      </div>
      
      <div className="col-lg-4 col-md-6 mb30">
      <div className="bloglist item">
            <div className="post-content">
                <div className="post-image">
                    <img alt="" src="./img/news/news-5.jpg" className="lazy"/>
                </div>
                <div className="post-text">
                    <span className="p-tagline">Tips &amp; Tricks</span>
                    <span className="p-date">October 28, 2020</span>
                    <h4><span>The next big trend in crypto<span></span></span></h4>
                    <p>Dolore officia sint incididunt non excepteur ea mollit commodo ut enim reprehenderit cupidatat labore ad laborum consectetur consequat...</p>
                    <span className="btn-main">Read more</span>
                </div>
            </div>
        </div>
      </div>
      
      <div className="col-lg-4 col-md-6 mb30">
        <div className="bloglist item">
              <div className="post-content">
                  <div className="post-image">
                      <img alt="" src="./img/news/news-6.jpg" className="lazy"/>
                  </div>
                  <div className="post-text">
                      <span className="p-tagline">Tips &amp; Tricks</span>
                      <span className="p-date">October 28, 2020</span>
                      <h4><span>The next big trend in crypto<span></span></span></h4>
                      <p>Dolore officia sint incididunt non excepteur ea mollit commodo ut enim reprehenderit cupidatat labore ad laborum consectetur consequat...</p>
                      <span className="btn-main">Read more</span>
                  </div>
              </div>
          </div>
      </div>

        <div className="spacer-single"></div>
                
        <ul className="pagination">
            <li><span className='a'>Prev</span></li>
            <li className="active"><span className='a'>1</span></li>
            <li><span className='a'>2</span></li>
            <li><span className='a'>3</span></li>
            <li><span className='a'>4</span></li>
            <li><span className='a'>5</span></li>
            <li><span className='a'>Next</span></li>
        </ul>
        
    </div>
  </section>

  <Footer />
</div>

);
export default news;