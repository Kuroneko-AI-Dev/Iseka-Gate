import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDwzRysDXR_cT41_MYFjKmeY1UsDN2X1AU",
  authDomain: "isekai-gate.firebaseapp.com",
  projectId: "isekai-gate",
  storageBucket: "isekai-gate.firebasestorage.app",
  messagingSenderId: "868967652387",
  appId: "1:868967652387:web:65e897a810629c94cb2596"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export const googleProvider =
    new GoogleAuthProvider();