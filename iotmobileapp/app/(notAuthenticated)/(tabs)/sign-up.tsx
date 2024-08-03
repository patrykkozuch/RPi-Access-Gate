import { useState } from "react";
import { TextInput, Button, StyleSheet } from "react-native";
import { View } from "../../../components/Themed";
import { useSession } from "../../../context/SessionProvider";

export default function SignUpPage(props: any) {
  const [state, setState] = useState({
    email: "",
    password: "",
  });
  const { signUp }: any = useSession();

  return (
    <View style={styles.container}>
      <>
        <TextInput
          style={styles.input}
          value={state.email}
          onChange={(e) => setState({ ...state, email: e.nativeEvent.text })}
          placeholder="Email"
          keyboardType="email-address"
        />
        <TextInput
          style={styles.input}
          value={state.password}
          onChange={(e) => setState({ ...state, password: e.nativeEvent.text })}
          placeholder="Password"
          secureTextEntry={true}
        />
        <Button
          title="Sign Up"
          onPress={() => {
            signUp(state.email, state.password);
          }}
        />
      </>
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
