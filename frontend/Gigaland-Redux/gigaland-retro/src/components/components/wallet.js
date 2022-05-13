import React from "react";
import { useState, useEffect, useContext } from "react";
import frontendAPI from "../../core/axios";
import {navigate} from "@reach/router";
import { signatureResult } from "../../xumm";

function Wallet({ setUserAccount }) {
  let [qrCode, setQrCode] = useState("");
  let [isConnecting, setIsConnecting] = useState(false);
  function handleClick(e) {
    e.preventDefault();
    setIsConnecting(true);
  }

  useEffect(
    function getUrl() {
      async function getQrcodeUrl() {
        let res = await frontendAPI.connectWallet();
        setQrCode(res.png_url);
        const signedPayload = await signatureResult(res.websocket);
        let backendRes = await frontendAPI.getUserXRPAccount(
          signedPayload.payload_uuidv4
        );
        console.log("Backend res", backendRes);
        while (backendRes.user === "not found") {
          backendRes = await frontendAPI.getUserXRPAccount(
            signedPayload.payload_uuidv4
          );
        }
        setUserAccount(backendRes.account);
        navigate("/");
      }
      if (isConnecting) {
        getQrcodeUrl();
      }
    },
    [isConnecting, setUserAccount]
  );
  return (
    <div className="row">
      {qrCode ? (
        <div className="mx-auto center mb30 col-lg-10 w-30">
          <span className="box-url center p-30 w-30">
            <img src={qrCode} alt=""></img>
            <p className="text-center text-nowrap text-font-weight-bold text-dark">
              please scan the QR code to connect wallet
            </p>
          </span>
        </div>
      ) : (
        <div className="col-lg-5 mb30 mx-auto center">
          <span className="box-url center mx-auto p-13">
            <span className="box-url-label">Most Popular</span>
            <a href="https://xumm.app/">
              <img src="./img/wallet/1.png" alt="" className="mb5 w-75" />
            </a>
            <h4>Xumm</h4>
            <p>
              Most Popular and user-friendly XRP wallet, developed by XRPL Labs
            </p>
            <button className="btn-dark mx-auto w-50" onClick={handleClick}>
              Connect Wallet
            </button>
          </span>
        </div>
      )}
    </div>
  );
}
export default Wallet;
