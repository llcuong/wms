import {StatusBar} from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';
import DetailScreen from './src/Home';
import "./global.css";

export default function App() {
    return (
        <View style={styles.container}>
            <DetailScreen />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
});
