import React from "react";
import { useStorageState } from "../hooks/useStorageState";
import { useRouter } from "expo-router";
import { signInRequest, signUpRequest, confirmSignUp } from "../services/auth";

const AuthContext = React.createContext<{
  signIn: (email: string, password: string) => void;
  signUp: (email: string, password: string) => void;
  activateAccount: (email: string, code: string) => void;
  signOut: () => void;
  session?: string | null;
  isLoading: boolean;
} | null>(null);

// This hook can be used to access the user info.
export function useSession() {
  const value = React.useContext(AuthContext);
  if (process.env.NODE_ENV !== "production") {
    if (!value) {
      throw new Error("useSession must be wrapped in a <SessionProvider />");
    }
  }

  return value;
}

export function SessionProvider(props: React.PropsWithChildren) {
  const router = useRouter();
  const [[isLoading, session], setSession] = useStorageState("session");

  return (
    <AuthContext.Provider
      value={{
        signIn: async (email, password) => {
          try {
            const result: any = await signInRequest(email, password);
            if (result.error) {
              throw result.message;
            }
            setSession(result.data.id_token);
          } catch (error) {
            alert(error);
          }
        },
        signUp: async (email, password) => {
          try {
            const result: any = await signUpRequest(email, password);
            if (result.error) {
              throw result.message;
            }

            router.replace("/(notAuthenticated)/activate-account");
          } catch (error) {
            alert(error);
          }
        },
        activateAccount: async (email, code) => {
          try {
            const result: any = await confirmSignUp(email, code);
            if (result.error) {
              throw result.message;
            }

            router.replace("/(notAuthenticated)/(tabs)/sign-in");
          } catch (err) {
            alert(err);
          }
        },
        signOut: () => {
          setSession(null);
        },
        session,
        isLoading,
      }}
    >
      {props.children}
    </AuthContext.Provider>
  );
}
