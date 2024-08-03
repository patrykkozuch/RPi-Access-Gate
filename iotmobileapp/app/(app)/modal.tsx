import {
  FlatList,
  View,
  Text,
  Alert,
  StyleSheet,
  Pressable,
  Modal,
  TextInput,
  Button,
} from "react-native";
import { Link, router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";
import WifiManager from "react-native-wifi-reborn";
import { PermissionsAndroid } from "react-native";
import Aes from "react-native-aes-crypto";
import { NetworkInfo } from "react-native-network-info";
import { useSession } from "../../context/SessionProvider";
import { pairRequest } from "../../services/auth";

export default function ModalPage() {
  const [wifiList, setWifiList] = useState<WifiManager.WifiEntry[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedSSID, setSelectedSSID] = useState<string>("");
  const [previousSSID, setPreviousSSID] = useState<string>("");
  const [predefinedIv, setPredefinedIv] = useState(
    "605f40ff8c98ae0abbd6c4d5057aa13c"
  );
  const [deviceId, setDeviceId] = useState<any>("");
  const [password, setPassword] = useState<string>("");
  const [key, setKey] = useState<any>("");
  const [iv, setIv] = useState<string>("");
  const isPresented = router.canGoBack();

  const { session }: any = useSession();

  const [predefinedSymmetricKey, setPredefinedSymmetricKey] = useState<any>(
    "955ffdd4e88b685b2978f8c58664f88a459e458737658e8b2acc7d0484f78742"
  );

  useEffect(() => {
    requestWIFIPermissions();
  }, []);

  const encryptData = (text: any, key: any, iv: any) => {
    return Aes.encrypt(text, key, iv, "aes-256-cbc").then((cipher) => ({
      cipher,
    }));
  };

  const decryptDataFromDevice = async (
    encryptedData: any,
    key: string,
    iv: string
  ) => {
    const d = await Aes.decrypt(encryptedData, key, iv, "aes-256-cbc");
    return d;
  };

  const requestWIFIPermissions = async () => {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: "Location permission is required for WiFi connections",
        message:
          "This app needs location permission as this is required  " +
          "to scan for wifi networks.",
        buttonNegative: "DENY",
        buttonPositive: "ALLOW",
      }
    );
    if (granted === PermissionsAndroid.RESULTS.GRANTED) {
      try {
        const wifiList = await WifiManager.loadWifiList();
        setWifiList(wifiList);
        setIv(await Aes.randomKey(16));
        setKey(await Aes.randomKey(32));
      } catch (e) {
        console.log(e);
      }
      // You can now use react-native-wifi-reborn
    } else {
      // Permission denied
    }
  };

  const connectToDevice = async () => {
    try {
      setPreviousSSID(await WifiManager.getCurrentWifiSSID());
      const data = `${selectedSSID},${password},${key},${iv}`;
      const encryptedData = await encryptData(
        data,
        predefinedSymmetricKey,
        predefinedIv
      );

      await WifiManager.connectToProtectedSSID(
        "IOT-HotSpot",
        "12345678",
        false,
        false
      );

      const ws = new WebSocket(
        `ws://${await NetworkInfo.getGatewayIPAddress()}:5678`
      );
      ws.onopen = () => {
        // Alert.alert((await WifiManager.connectionStatus()).toString());
        // // Encrypt and send data

        // Alert.alert(encryptedData.cipher);
        ws.send(encryptedData.cipher);
      };

      const handleData = async (data: any) => {
        const decr = await decryptDataFromDevice(data, key, iv);
        setDeviceId(decr);
        ws.close();
        await WifiManager.disconnect();
        while (!(await WifiManager.connectionStatus())) {}
        const res: any = await pairRequest(decr, key, iv, session);
        if (res.success) {
          Alert.alert("Device paired successfully");
          router.push("/(app)/(tabs)");
        }
      };

      ws.onmessage = (e) => {
        handleData(e.data).then();
      };

      ws.onclose = () => {};
    } catch (err: any) {
      Alert.alert(err.message);
    }
  };

  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      {!isPresented && <Link href="../">Dismiss</Link>}
      <StatusBar style="light" />
      <TextInput
        style={styles.input}
        onChangeText={(text: any) => setSelectedSSID(text)}
        value={selectedSSID}
        placeholder="SSID"
      />
      <TextInput
        style={styles.input}
        onChangeText={(text: any) => setPassword(text)}
        value={password}
        placeholder="PASSWORD"
        secureTextEntry
      />
      <Button title="Add Device" onPress={() => setModalVisible(true)} />
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          Alert.alert("Modal has been closed.");
          setModalVisible(!modalVisible);
        }}
      >
        <View style={styles.centeredView}>
          <View style={styles.modalView}>
            <Text style={styles.modalText}>How to connect to your device?</Text>
            <Text>1. Press button on your device</Text>
            <Text>2. Wait until LED turns blue on device</Text>
            <Text>3. Press Connect</Text>
            <Pressable
              style={[styles.button, styles.buttonClose]}
              onPress={async () => {
                connectToDevice();
              }}
            >
              <Text style={styles.textStyle}>Connect</Text>
            </Pressable>
            <Pressable
              style={[styles.button, styles.buttonClose]}
              onPress={() => setModalVisible(!modalVisible)}
            >
              <Text style={styles.textStyle}>Hide Modal</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  input: {
    marginBottom: 10,
    borderColor: "black",
    borderWidth: 1,
    width: 200,
    height: 40,
    borderRadius: 10,
    padding: 5,
  },
  centeredView: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    marginTop: 22,
  },
  modalView: {
    margin: 20,
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  button: {
    borderRadius: 20,
    padding: 10,
    elevation: 2,
    margin: 5,
  },
  buttonOpen: {
    backgroundColor: "#F194FF",
  },
  buttonClose: {
    backgroundColor: "#2196F3",
  },
  textStyle: {
    color: "white",
    fontWeight: "bold",
    textAlign: "center",
  },
  modalText: {
    marginBottom: 15,
    textAlign: "center",
  },
});
