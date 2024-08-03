import { useLocalSearchParams, useRouter } from "expo-router";
import { FlatList, Text, View, StyleSheet, Button } from "react-native";
import { forgotDevice, getDeviceLogs } from "../../../services/auth";
import { useState, useEffect } from "react";
import { useSession } from "../../../context/SessionProvider";

export default function Page() {
  const { slug }: any = useLocalSearchParams();
  const [deviceLogs, setDeviceLogs] = useState<any[]>([]);

  const { session }: any = useSession();
  const router = useRouter();

  async function fetchDeviceLogs() {
    const result: any = await getDeviceLogs(session, slug);
    if (result.success) {
      setDeviceLogs(result.data);
    }
  }

  useEffect(() => {
    fetchDeviceLogs();
  }, []);

  return (
    <View>
      <Button
        onPress={async () => {
          const result: any = await forgotDevice(session, slug);
          if (result.success) {
            router.push("/(app)/(tabs)");
          }
        }}
        title={"Forgot this device"}
      />
      <Text>Logs from Device: {slug}</Text>
      <FlatList
        data={deviceLogs}
        keyExtractor={(item, index) => "key" + index}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>Tag ID: {item.tagId}</Text>
            <Text>Device ID: {item.deviceId}</Text>
            <Text>User ID: {item.userId}</Text>
          </View>
        )}
      />
      <Button onPress={fetchDeviceLogs} title={"Reload logs"} />
    </View>
  );
}

const styles = StyleSheet.create({
  item: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
});
