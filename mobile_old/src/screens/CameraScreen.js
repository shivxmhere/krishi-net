import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator, Alert, SafeAreaView } from 'react-native';
import { Camera } from 'expo-camera';
import { useNavigation } from '@react-navigation/native';
import api from '../services/api';

export default function CameraScreen() {
    const [hasPermission, setHasPermission] = useState(null);
    const [loading, setLoading] = useState(false);
    const cameraRef = useRef(null);
    const navigation = useNavigation();

    useEffect(() => {
        (async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            setHasPermission(status === 'granted');
        })();
    }, []);

    const takePicture = async () => {
        if (cameraRef.current) {
            setLoading(true);
            try {
                const photo = await cameraRef.current.takePictureAsync({ quality: 0.7 });
                await uploadImage(photo.uri);
            } catch (error) {
                console.error("Error taking picture:", error);
                Alert.alert("Error", "Could not capture image.");
                setLoading(false);
            }
        }
    };

    const uploadImage = async (uri) => {
        const formData = new FormData();
        formData.append('file', {
            uri: uri,
            type: 'image/jpeg',
            name: 'upload.jpg',
        });

        try {
            // Using centralized api service which handles the Authorization header
            const response = await api.post('/api/detect', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setLoading(false);
            navigation.navigate('Result', { data: response.data });
        } catch (error) {
            console.error("Upload error:", error);
            setLoading(false);

            const errorMsg = error.response?.data?.detail || "Failed to analyze image. Please try again.";
            Alert.alert("Analysis Failed", errorMsg);
        }
    };

    if (hasPermission === null) {
        return <View style={styles.centered}><ActivityIndicator size="large" color="#2e7d32" /></View>;
    }
    if (hasPermission === false) {
        return <View style={styles.centered}><Text>No access to camera. Please enable it in settings.</Text></View>;
    }

    return (
        <SafeAreaView style={styles.container}>
            <Camera style={styles.camera} ref={cameraRef}>
                <View style={styles.overlay}>
                    <View style={styles.guideContainer}>
                        <View style={styles.guideBox} />
                        <Text style={styles.guideText}>Center the leaf in the square</Text>
                    </View>

                    <View style={styles.bottomBar}>
                        {loading ? (
                            <ActivityIndicator size="large" color="#ffffff" />
                        ) : (
                            <TouchableOpacity style={styles.captureBtn} onPress={takePicture}>
                                <View style={styles.captureRing}>
                                    <View style={styles.captureCircle} />
                                </View>
                            </TouchableOpacity>
                        )}
                    </View>
                </View>
            </Camera>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000',
    },
    centered: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    camera: {
        flex: 1,
    },
    overlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.2)',
        justifyContent: 'space-between',
        padding: 40,
    },
    guideContainer: {
        alignItems: 'center',
        marginTop: 100,
    },
    guideBox: {
        width: 250,
        height: 250,
        borderWidth: 2,
        borderColor: '#fff',
        borderRadius: 20,
        borderStyle: 'dashed',
    },
    guideText: {
        color: '#fff',
        marginTop: 20,
        fontSize: 16,
        fontWeight: 'bold',
        textShadowColor: 'rgba(0,0,0,0.5)',
        textShadowOffset: { width: 1, height: 1 },
        textShadowRadius: 3,
    },
    bottomBar: {
        alignItems: 'center',
        marginBottom: 20,
    },
    captureBtn: {
        alignItems: 'center',
    },
    captureRing: {
        width: 80,
        height: 80,
        borderRadius: 40,
        borderWidth: 4,
        borderColor: '#fff',
        justifyContent: 'center',
        alignItems: 'center',
    },
    captureCircle: {
        width: 65,
        height: 65,
        borderRadius: 32.5,
        backgroundColor: '#fff',
    },
});
