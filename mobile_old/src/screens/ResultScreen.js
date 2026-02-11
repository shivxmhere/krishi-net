import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';

export default function ResultScreen({ route, navigation }) {
    const { data } = route.params;

    const getSeverityColor = (severity) => {
        switch (severity?.toUpperCase()) {
            case 'HIGH': return '#d32f2f';
            case 'MEDIUM': return '#f57c00';
            case 'LOW': return '#388e3c';
            default: return '#757575';
        }
    };

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView contentContainerStyle={styles.scrollContent}>
                <View style={styles.card}>
                    <View style={styles.header}>
                        <Text style={styles.label}>ANALYSIS RESULT</Text>
                        <View style={[styles.badge, { backgroundColor: getSeverityColor(data.severity) }]}>
                            <Text style={styles.badgeText}>{data.severity || 'UNKNOWN'}</Text>
                        </View>
                    </View>

                    <Text style={styles.diseaseName}>{data.disease_name}</Text>
                    <Text style={styles.hindiName}>{data.disease_name_hi || "Localized name unavailable"}</Text>

                    <View style={styles.statsRow}>
                        <View style={styles.statBox}>
                            <Text style={styles.statLabel}>Confidence</Text>
                            <Text style={styles.statValue}>{(data.confidence * 100).toFixed(1)}%</Text>
                        </View>
                        <View style={styles.statBox}>
                            <Text style={styles.statLabel}>Status</Text>
                            <Text style={[styles.statValue, { color: getSeverityColor(data.severity) }]}>
                                {data.severity === 'HEALTHY' ? 'Safe' : 'Action Needed'}
                            </Text>
                        </View>
                    </View>

                    <View style={styles.section}>
                        <Text style={styles.sectionTitle}>Recommended Treatment</Text>
                        {data.treatment && data.treatment.steps && data.treatment.steps.length > 0 ? (
                            data.treatment.steps.map((step, index) => (
                                <View key={index} style={styles.stepRow}>
                                    <View style={styles.stepNumber}>
                                        <Text style={styles.stepNumberText}>{index + 1}</Text>
                                    </View>
                                    <Text style={styles.stepText}>{step}</Text>
                                </View>
                            ))
                        ) : (
                            <Text style={styles.emptyText}>No specific treatment steps found. Please consult a local agricultural officer.</Text>
                        )}
                    </View>
                </View>

                <TouchableOpacity
                    style={styles.actionBtn}
                    onPress={() => navigation.navigate('Home')}
                >
                    <Text style={styles.actionBtnText}>Back to Dashboard</Text>
                </TouchableOpacity>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f7f5',
    },
    scrollContent: {
        padding: 20,
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 24,
        padding: 24,
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 10,
        marginBottom: 25,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 15,
    },
    label: {
        fontSize: 12,
        fontWeight: 'bold',
        color: '#999',
        letterSpacing: 1,
    },
    badge: {
        paddingHorizontal: 12,
        paddingVertical: 4,
        borderRadius: 8,
    },
    badgeText: {
        color: '#fff',
        fontSize: 12,
        fontWeight: 'bold',
    },
    diseaseName: {
        fontSize: 26,
        fontWeight: 'bold',
        color: '#2c3e50',
        marginBottom: 4,
    },
    hindiName: {
        fontSize: 18,
        color: '#7f8c8d',
        marginBottom: 24,
    },
    statsRow: {
        flexDirection: 'row',
        backgroundColor: '#f9f9f9',
        borderRadius: 16,
        padding: 15,
        marginBottom: 30,
    },
    statBox: {
        flex: 1,
        alignItems: 'center',
    },
    statLabel: {
        fontSize: 12,
        color: '#666',
        marginBottom: 5,
    },
    statValue: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333',
    },
    section: {
        marginTop: 10,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1b5e20',
        marginBottom: 15,
    },
    stepRow: {
        flexDirection: 'row',
        marginBottom: 16,
        alignItems: 'flex-start',
    },
    stepNumber: {
        width: 24,
        height: 24,
        borderRadius: 12,
        backgroundColor: '#e8f5e9',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 12,
        marginTop: 2,
    },
    stepNumberText: {
        fontSize: 12,
        fontWeight: 'bold',
        color: '#2e7d32',
    },
    stepText: {
        flex: 1,
        fontSize: 16,
        color: '#444',
        lineHeight: 24,
    },
    emptyText: {
        fontSize: 16,
        color: '#7f8c8d',
        fontStyle: 'italic',
    },
    actionBtn: {
        backgroundColor: '#2e7d32',
        borderRadius: 16,
        padding: 18,
        alignItems: 'center',
    },
    actionBtnText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
});
