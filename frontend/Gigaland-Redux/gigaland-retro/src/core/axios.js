import axios from "axios";

export const Axios = axios.create();
export const Canceler = axios.CancelToken.source();

// FLASK url
const BASE_URL = "http://127.0.0.1:5000/";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 * There shouldn't be any frontend-specific stuff here, and there shouldn't
 * be any API-aware stuff elsewhere in the frontend.
 *
 */

class frontendAPI {
  // the token for interactive with the API will be stored here.
  static token;

  static async request(endpoint, data = {}, method = "get", hasImage = false) {
    console.debug("API Call:", endpoint, data, method);

    const url = `${BASE_URL}/${endpoint}`;
    const headers = { Authorization: `Bearer ${frontendAPI.token}` };
    if (hasImage) {
      headers["Content-Type"] = "multipart/form-data";
    }
    const params = method === "get" ? data : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err) {
      console.error("API Error:", err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }

  // Individual API routes

  // /* login  */
  // static async login(userData) {
  //   const res = await this.request(`auth/token`, { ...userData }, "post");
  //   return res.token;
  // }

  // /* signup */
  // static async signup(userData) {
  //   const res = await this.request(`auth/register`, { ...userData }, "post");
  //   return res.token;
  // }

  // /* get the user given the username and token */
  // static async getUser(username) {
  //   const res = await this.request(`users/${username}`);
  //   return res.user;
  // }

  // /* update the user given with user inputted form data */
  // static async updateProfile(userData) {
  //   const data = {
  //     firstName: userData.firstName,
  //     lastName: userData.lastName,
  //     email: userData.email,
  //     password: userData.password,
  //   };

  //   const res = await this.request(`users/${userData.username}`, data, "patch");
  //   return res.user;
  // }

  /** Get details on an NFT by tokenID. */


  static async connectWallet() {
    const res = await this.request(`users/connect-wallet`, {}, "get");
    return res;
  }



  static async getNFT(id) {
    const res = await this.request(`api/nfts/${id}`);
    return res.nft;
  }

  /** Get all nfts. */

  static async getNFTs() {
    const res = await this.request(`api/nfts`);
    return res.nft;
  }

  /* submit nft mint request and show QR code */
  static async mintNFT(data) {
    const res = await this.request(`api/nfts/mint`, data, "post", true);
    return res.pushed;
  }

  /* submit nft mint request and show QR code */
  static async editNFT(id, data) {
    const res = await this.request(`api/nfts/${id}/edit`, data, "put");
    return res.pushed;
  }

  /** Get details on an auction by ID. */

  static async getAuction(id) {
    const res = await this.request(`api/auctions/${id}`);
    return res.auction;
  }

  /** Get all auctions */
  static async getAuctions() {
    const res = await this.request(`api/auctions`);
    return res.auctions;
  }

  /** Submit a new bid on a certain auction given id */
  static async submitNewBid(id, xrp_address, price) {
    const res = await this.request(
      `api/auctions/${id}/new_bid}`,
      { buyer: xrp_address, price: price },
      "post"
    );
    return res.auctions;
  }

  /* TODO: end-auction API call
    seller still has to sign
  

  
  */
  static async extendAuction(id, end_at) {
    const res = await this.request(
      `api/auctions/${id}/extend}`,
      { end_at },
      "patch"
    );
    return res.auction;
  }

  static async deleteAuction(id) {
    const res = await this.request(`api/auctions/${id}/cancel}`, "delete");
    return res.msg;
  }
}

// for now, put token ("testuser" / "password" on class)
frontendAPI.token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZ" +
  "SI6InRlc3R1c2VyIiwiaXNBZG1pbiI6ZmFsc2UsImlhdCI6MTU5ODE1OTI1OX0." +
  "FtrMwBQwe6Ue-glIFgz_Nf8XxRT2YecFCiSpYL0fCXc";

export default frontendAPI;
