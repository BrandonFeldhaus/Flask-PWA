/// Registers the service worker
(function() {
  if('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js')
               .then(function(registration) {
               console.log('Service Worker Registered');
               return registration;
      })
      .catch(function(err) {
        console.error('Unable to register service worker.', err);
      });
      navigator.serviceWorker.ready.then(function(registration) {
        console.log('Service Worker Ready');
      });
    });
  }
})();

let deferredPrompt = null;
const btnAdd = document.getElementById('installButton');

/// Checks to make sure if its been installed or not
window.addEventListener('beforeinstallprompt', (e) => {
  console.log('beforeinstallprompt event fired');
  e.preventDefault();
  deferredPrompt = e;
  btnAdd.style.visibility = 'visible';
});

/// If there is a button and it is clicked, display install prompt and install if users chooses too
if(btnAdd){
      btnAdd.addEventListener('click', (e) => {
      btnAdd.style.visibility = 'hidden';
      deferredPrompt.prompt();
      deferredPrompt.userChoice
        .then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('User accepted the A2HS prompt');
          } else {
            console.log('User dismissed the A2HS prompt');
          }
          deferredPrompt = null;
        });
    });
}

///
window.addEventListener('appinstalled', (evt) => {
  btnAdd.style.visibility = 'hidden';
  app.logEvent('app', 'installed');
});

if (window.matchMedia('(display-mode: standalone)').matches) {
  btnAdd.style.visibility = 'hidden';
  console.log('display-mode is standalone');
}

///// Request permission to notify the user
/////
/////
const pushButton = document.getElementById('push-btn');

if (!("Notification" in window)) {
    pushButton.hidden;
}

pushButton.addEventListener('click', askPermission);

function askPermission(evt) {
  pushButton.disabled = true;
  Notification.requestPermission().then(function(permission) {
    notificationButtonUpdate();
   });
}

function notificationButtonUpdate() {
  if(Notification.permission === 'granted') {
    pushButton.disabled = true;
  } else {
    pushButton.disabled = false;
  }
}


/// Request permission to retrieve the location of the user
if ('geolocation' in navigator) {
  document.getElementById('askLocation').addEventListener('click', function () {
    navigator.geolocation.getCurrentPosition(function (location) {
      console.log(location);
    });
  });
} else {
  console.log('Geolocation API not supported.');
}