import { Button, StyleSheet, TextInput } from "react-native";
import { View } from "../../../components/Themed";
import { useState } from "react";
import { confirmResetPassword, resetPassword } from "../../../services/auth";

export default function ForgotPasswordPage() {
  const [state, setState] = useState({
    email: "",
    code: "",
    password: "",
  });

  const [step, setStep] = useState(0);

  return (
    <View style={styles.container}>
      {step === 0 && (
        <>
          <TextInput
            style={styles.input}
            onChangeText={(text: any) => setState({ ...state, email: text })}
            value={state.email}
            placeholder="Email"
          />
          <Button
            title="Reset password"
            onPress={async () => {
              const response: any = await resetPassword(state.email);

              if (response.error) {
                alert(response.message);
                return;
              }

              setStep(1);
            }}
          />
        </>
      )}

      {step === 1 && (
        <>
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
          <TextInput
            style={styles.input}
            secureTextEntry
            onChangeText={(text: any) => setState({ ...state, password: text })}
            value={state.password}
            placeholder="New password"
          />
          <Button
            title="Confirm reset password"
            onPress={async () => {
              const response: any = await confirmResetPassword(
                state.email,
                state.code,
                state.password
              );

              if (response.error) {
                alert(response.message);
              } else {
                alert("Password reset successfully!");
              }

              setStep(0);
              setState({
                email: "",
                code: "",
                password: "",
              });
            }}
          />
        </>
      )}
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
