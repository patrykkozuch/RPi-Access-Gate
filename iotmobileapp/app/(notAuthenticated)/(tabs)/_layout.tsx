import FontAwesome from "@expo/vector-icons/FontAwesome";
import { Tabs } from "expo-router";
import { useColorScheme } from "react-native";

import Colors from "../../../constants/Colors";
/**
 * You can explore the built-in icon families and icons on the web at https://icons.expo.fyi/
 */
function TabBarIcon(props: {
  name: React.ComponentProps<typeof FontAwesome>["name"];
  color: string;
}) {
  return <FontAwesome size={28} style={{ marginBottom: -3 }} {...props} />;
}

export default function TabLayout() {
  const colorScheme = useColorScheme();
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? "light"].tint,
      }}
    >
      <Tabs.Screen
        name="sign-in"
        options={{
          title: "Sign In",
          tabBarIcon: ({ color }) => <TabBarIcon name="code" color={color} />,
        }}
      />
      <Tabs.Screen
        name="sign-up"
        options={{
          title: "Sign Up",
          tabBarIcon: ({ color }) => <TabBarIcon name="code" color={color} />,
        }}
      />
      <Tabs.Screen
        name="forgot-password"
        options={{
          title: "Forgot Password",
          tabBarIcon: ({ color }) => <TabBarIcon name="code" color={color} />,
        }}
      />
    </Tabs>
  );
}
