import axios from "axios";
import { Alert } from "react-native";

export const resetPassword = async (email: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//auth/reset-password",
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        email: email,
      },
    })
      .then((result: any) => {
        resolve(result.data);
      })
      .catch((error: any) => reject(error));
  });
};

export const confirmResetPassword = async (
  email: string,
  code: string,
  password: string
) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//auth/confirm-reset-password",
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        email: email,
        code: code,
        password: password,
      },
    })
      .then((result: any) => {
        resolve(result.data);
      })
      .catch((error: any) => reject(error));
  });
};

export const resendActivationCode = async (email: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//auth/resend-code",
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        email: email,
      },
    })
      .then((result: any) => {
        resolve(result.data);
      })
      .catch((error: any) => reject(error));
  });
};

export const signInRequest = async (email: string, password: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//auth/sign-in",
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        email: email,
        password: password,
      },
    })
      .then((result: any) => {
        resolve(result.data);
      })
      .catch((error: any) => reject(error));
  });
};

export const signUpRequest = async (email: string, password: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//auth/sign-up",
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        email: email,
        password: password,
      },
    })
      .then((result: any) => resolve(result.data))
      .catch((error: any) => reject(error));
  });
};

export const confirmSignUp = async (email: string, code: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//auth/confirm-sign-up",
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        email: email,
        code: code,
      },
    })
      .then((result: any) => resolve(result.data))
      .catch((error: any) => reject(error));
  });
};

export const pairRequest = async (
  deviceId: string,
  key: string,
  iv: string,
  token: string
) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//pair/app",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
      data: {
        deviceId: deviceId,
        key: key,
        iv: iv,
      },
    })
      .then((result: any) => resolve(result.data))
      .catch((error: any) => reject(error));
  });
};

export const getPairedDevices = async (token: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "GET",
      url: "https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//app/devices",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    })
      .then((result: any) => resolve(result.data))
      .catch((error: any) => reject(error));
  });
};

export const getDeviceLogs = async (token: string, deviceId: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "GET",
      url: `https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//app/devices/${deviceId}/access-log`,
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    })
      .then((result: any) => resolve(result.data))
      .catch((error: any) => reject(error));
  });
};

export const forgotDevice = async (token: string, deviceId: string) => {
  return new Promise((resolve, reject) => {
    axios({
      method: "POST",
      url: `https://rb3jg63dj0.execute-api.us-east-1.amazonaws.com/prod//unpair`,
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
      data: {
        deviceId: deviceId,
      },
    })
      .then((result: any) => resolve(result.data))
      .catch((error: any) => reject(error));
  });
};
