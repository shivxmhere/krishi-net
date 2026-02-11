import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView, Dimensions } from 'react-native';
import { useAuth } from '../contexts/AuthContext';

const { width } = Dimensions.get('window');

export default function HomeScreen({ navigation }) {
    const { user, logout } = useAuth();

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.content}>
                <View style={styles.header}>
                    <Text style={styles.welcome}>Welcome,</Text>
                    <Text style={styles.username}>{user?.email?.split('@')[0]}</Text>
                </View>

                <View style={styles.heroCard}>
                    <Text style={styles.heroEmoji}>🌾</Text>
                    <Text style={styles.heroTitle}>Keep your crops healthy</Text>
                    <Text style={styles.heroSubtitle}>Use our AI to detect diseases in seconds and get expert tips.</Text>
                </View>

                <View style={styles.actionContainer}>
                    <TouchableOpacity
                        style={styles.mainButton}
                        onPress={() => navigation.navigate('Camera')}
                    >
                        <Text style={styles.mainButtonEmoji}>📷</Text>
                        <Text style={styles.mainButtonText}>Scan New Crop</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                        style={styles.secondaryButton}
                        onPress={logout}
                    >
                        <Text style={styles.secondaryButtonText}>Sign Out</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    content: {
        flex: 1,
        padding: 25,
    },
    header: {
        marginTop: 20,
        marginBottom: 30,
    },
    welcome: {
        fontSize: 18,
        color: '#666',
    },
    username: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#2e7d32',
    },
    heroCard: {
        backgroundColor: '#e8f5e9',
        borderRadius: 24,
        padding: 25,
        alignItems: 'center',
        marginBottom: 40,
    },
    heroEmoji: {
        fontSize: 60,
        marginBottom: 15,
    },
    heroTitle: {
        fontSize: 22,
        fontWeight: 'bold',
        color: '#1b5e20',
        textAlign: 'center',
        marginBottom: 8,
    },
    heroSubtitle: {
        fontSize: 15,
        color: '#4caf50',
        textAlign: 'center',
        lineHeight: 22,
    },
    actionContainer: {
        flex: 1,
        justifyContent: 'flex-end',
        paddingBottom: 20,
    },
    mainButton: {
        backgroundColor: '#2e7d32',
        borderRadius: 18,
        padding: 20,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        elevation: 4,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.2,
        shadowRadius: 8,
    },
    mainButtonEmoji: {
        fontSize: 24,
        marginRight: 12,
    },
    mainButtonText: {
        color: '#fff',
        fontSize: 20,
        fontWeight: 'bold',
    },
    secondaryButton: {
        marginTop: 20,
        alignSelf: 'center',
        padding: 10,
    },
    secondaryButtonText: {
        color: '#d32f2f',
        fontSize: 16,
        fontWeight: '600',
    },
});
