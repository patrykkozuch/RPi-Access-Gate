import { Button, StyleSheet, TextInput } from "react-native";
import { View } from "../../components/Themed";
import { useState } from "react";
import { useSession } from "../../context/SessionProvider";
import { resendActivationCode } from "../../services/auth";
import { useRouter } from "expo-router";

export default function ActivateAccount() {
  const router = useRouter();
  const { activateAccount }: any = useSession();

  const [state, setState] = useState({
    email: "",
    code: "",
  });

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        onChangeText={(text: any) => setState({ ...state, email: text })}
        value={state.email}
        placeholder="Email"
      />
      <TextInput
        style={styles.input}
        onChangeText={(text: any) => setState({ ...state, code: text })}
        value={state.code}
        placeholder="Code"
      />
      <Button
        title="Activate account"
        onPress={() => {
          activateAccount(state.email, state.code);
        }}
      />
      <Button
        title="Resend code"
        onPress={async () => {
          const response: any = await resendActivationCode(state.email);

          if (response.error) {
            alert(response.message);
            return;
          }

          alert("Code sent");
        }}
      />
      <Button
        title="Go back"
        onPress={() => router.push("/(notAuthenticated)/(tabs)/sign-up")}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: "80%",
  },
  input: {
    marginBottom: 10,
    borderColor: "black",
    borderWidth: 1,
    width: 200,
    height: 40,
    borderRadius: 10,
    padding: 5,
  },
});
