// Specific Version Compatibility
(function () {
  var COMPAT_ENVS = [
    ['Firefox', ">= 16.0"],
    ['Google Chrome',
     ">= 24.0 (you may need to get Google Chrome Canary), NO Blob storage support"]
  ];
  var compat = $('#compat');
  compat.empty();
  compat.append('<ul id="compat-list"></ul>');
  COMPAT_ENVS.forEach(function(val, idx, array) {
    $('#compat-list').append('<li>' + val[0] + ': ' + val[1] + '</li>');
})();

const DB_NAME = 'MyTestDatabase';
const DB_VERSION = 3; // Use a long long for this value (don't use a float)
const DB_STORE_NAME = 'Users';

var db;

// Used to keep track of which view is displayed to avoid uselessly reloading it
var current_view_pub_key;

//Check for support (browser support)
if (!('indexedDB' in window)) {
    console.log('This browser doesn\'t support IndexedDB');
    return;
}

function openDb() {
    console.log("Opening Db ...");
    var req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onsuccess = function (evt) {
      // Equal to: db = req.result;
      db = this.result;
      console.log("Opening Db DONE");
    };
    req.onerror = function (evt) {
      console.error("openDb:", evt.target.errorCode);
    };

    //Anytime the IndexedDB database needs to be upgraded, everything needs to be copied over.
    request.onupgradeneeded = function(event) {
      // Save the IDBDatabase interface
      var db = event.target.result;

      // Create an objectStore for this database called "name"
      var objectStore = db.createObjectStore(DB_STORE_NAME, {keyPath: 'id', autoIncrement:true});

      // Create an index to search users by name. We may have duplicates
      // so we can't use a unique index.
      objectStore.createIndex("name", "name", { unique: false });

      // Create an index to search users by email. We want to ensure that
      // no two customers have the same email, so use a unique index.
      objectStore.createIndex("email", "email", { unique: true })

      // Create an index to search users by DOBs. We may have duplicates
      // so we can't use a unique index
      objectStore.createIndex("dateOfBirth", "dateOfBirth", {unique: false})
    };
};

/**
* @param {string} store_name
* @param {string} mode either "readonly" or "readwrite"
*/
function getObjectStore(store_name, mode) {
var tx = db.transaction(store_name, mode);
return tx.objectStore(store_name);
}

function clearObjectStore() {
var store = getObjectStore(DB_STORE_NAME, 'readwrite');
var req = store.clear();
    req.onsuccess = function(evt) {
      displayActionSuccess("Store cleared");
      displayPubList(store);
    };
    req.onerror = function (evt) {
      console.error("clearObjectStore:", evt.target.errorCode);
      displayActionFailure(this.error);
    };
}

function getBlob(key, store, success_callback) {
    var req = store.get(key);
    req.onsuccess = function(evt) {
    var value = evt.target.result;
    if (value)
        success_callback(value.blob);
    };
}

/**
* @param {string} name
* @param {string} email
* @param {string} dateOfBirth
* @param {Blob=} blob
*/
function addUser(name, email, dateOfBirth, blob) {
console.log("addUser arguments:", arguments);
var obj = { name: name, email: email, dateOfBirth: dateOfBirth };
if (typeof blob != 'undefined')
  obj.blob = blob;
}