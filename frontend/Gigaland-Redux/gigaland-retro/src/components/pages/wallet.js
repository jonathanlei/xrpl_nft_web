import React from "react";
import Wallet from "../components/wallet";
import Footer from "../components/footer";

const wallet = ({ setUserAccount }) => (
  <div>
    <section className="jumbotron breadcumb no-bg">
      <div className="mainbreadcumb">
        <div className="container">
          <div className="row m-10-hor">
            <div className="col-12">
              <h1 className="text-center">Wallet</h1>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section className="container">
      <Wallet setUserAccount={setUserAccount} />
    </section>

    <Footer />
  </div>
);
export default wallet;
