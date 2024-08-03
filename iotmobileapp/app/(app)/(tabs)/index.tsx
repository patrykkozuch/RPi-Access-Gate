import { Link } from "expo-router";
import React, { useEffect, useState } from "react";
import { Text, View, StyleSheet, FlatList, Button } from "react-native";
import { getPairedDevices } from "../../../services/auth";
import { useSession } from "../../../context/SessionProvider";

export default function UserPage() {
  const [devices, setDevices] = useState<string[]>([]);
  const { session }: any = useSession();

  async function fetchDevices() {
    const result: any = await getPairedDevices(session);
    console.log(result);
    if (result.success) {
      setDevices(result.data);
    }
  }

  useEffect(() => {
    fetchDevices();
  }, []);

  return (
    <View style={styles.container}>
      <Text>Paired devices</Text>
      <FlatList
        data={devices}
        keyExtractor={(item) => item}
        renderItem={({ item }) => (
          <Link href={`/(app)/device/${item}`}>
            <View style={styles.item}>
              <Text>Device ID: {item}</Text>
            </View>
          </Link>
        )}
      />
      <Button title={"reload"} onPress={fetchDevices} />

      <Link
        href="/modal"
        style={{ backgroundColor: "blue", color: "white", padding: 10 }}
      >
        Add new device
      </Link>
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
    fontSize: 24,
    fontWeight: "bold",
  },
  text: {
    fontSize: 18,
  },
  item: {
    padding: 20,
    borderWidth: 1,
    borderColor: "black",
  },
});
