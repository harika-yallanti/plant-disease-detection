import { initializeApp } from
    "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";

import { getAuth } from
    "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";
    
const firebaseConfig = {
  apiKey: "AIzaSyDtzBYH57K1nTbNAgB55OIgKXOLV9UvYkY",
  authDomain: "plantcare-ai-b9fc0.firebaseapp.com",
  projectId: "plantcare-ai-b9fc0",
  storageBucket: "plantcare-ai-b9fc0.firebasestorage.app",
  messagingSenderId: "273561013788",
  appId: "1:273561013788:web:618407757aae75165859d9",
  measurementId: "G-WLKZ91QYDG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);


// Initialize Firebase Authentication
const auth = getAuth(app);


// Export Firebase instances
export {
    app,
    auth
};