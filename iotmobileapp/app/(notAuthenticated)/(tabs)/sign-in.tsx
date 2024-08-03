import { Button, StyleSheet, TextInput } from "react-native";
import { View } from "../../../components/Themed";
import { useState } from "react";
import { useSession } from "../../../context/SessionProvider";

export default function SignInPage() {
  const { signIn }: any = useSession();

  const [state, setState] = useState({
    email: "",
    password: "",
  });

  return (
    <View style={styles.container}>
      <>
        <TextInput
          style={styles.input}
          onChangeText={(text: any) => setState({ ...state, email: text })}
          value={state.email}
          placeholder="Email"
        />
        <TextInput
          style={styles.input}
          onChangeText={(text: any) => setState({ ...state, password: text })}
          value={state.password}
          placeholder="Password"
          secureTextEntry
        />
        <Button
          title="Sign In"
          onPress={() => {
            signIn(state.email, state.password);
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
