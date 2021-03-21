'use strict'

const uuidv4 = require('uuid/v4');
const crypto = require('crypto');

//const apiKey = '';
//const apiSecret = '';
var body = {
    "postOnly":true,
    "mode":"market",
    "offerType":"BUY",
    "amount":1,
    "price":50,
    "fillOrKill":false
}

function getHash(apiKey, timestamp, apiSecret, body) {
    const hmac = crypto.createHmac('sha512', apiSecret);
    console.log("TIMESTAMP " + timestamp)
    let inputData = "";
    if (body) {
        inputData = apiKey + timestamp + JSON.stringify(body);
        hmac.update(inputData);
    }
    else {
        inputData =apiKey + timestamp;
        hmac.update(inputData);
    }
    const apihash =  hmac.digest('hex');
    console.log(inputData);
    console.log(apihash);
    return apihash;
};

//let timestamp = Date.now();
let timestamp = "1616271407";
const apihash = getHash(apiKey, timestamp, apiSecret, body)
var headers = {
    'API-Key': apiKey,
    'API-Hash': apihash,
    'operation-id': uuidv4(),
    'Request-Timestamp': timestamp,
    'Content-Type': 'application/json'
};