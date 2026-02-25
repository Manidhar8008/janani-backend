import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';

export default function HomeScreen() {
  const router = useRouter();
  const [hour, setHour] = useState(new Date().getHours());
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    const updateTime = setInterval(() => {
      const now = new Date().getHours();
      setHour(now);
    }, 60000); // Update every minute
    return () => clearInterval(updateTime);
  }, []);

  useEffect(() => {
    if (hour < 12) {
      setGreeting('🌅 MORNING');
    } else if (hour < 21) {
      setGreeting('🌆 EVENING');
    } else {
      setGreeting('🌙 NIGHT');
    }
  }, [hour]);

  return (
    <ScrollView style={styles.scroll}>
      <View style={styles.container}>
        <Text style={styles.label}>✦ PERSONAL INTELLIGENCE ENGINE ✦</Text>
        <Text style={styles.title}>Janani.AI</Text>
        <Text style={styles.subtitle}>She watches. She knows.{'\n'}She unlocks you.</Text>
        
        <Text style={styles.timeGreeting}>{greeting}</Text>

        <TouchableOpacity 
          style={styles.btn}
          onPress={() => router.push('/morning')}>
          <Text style={styles.btnText}>BEGIN MORNING CHECK-IN</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.btn}
          onPress={() => router.push('/diary')}>
          <Text style={styles.btnText}>UPDATE DIARY</Text>
        </TouchableOpacity>

        {hour >= 21 && (
          <View style={styles.scheduleBox}>
            <Text style={styles.scheduleTitle}>📋 TOMORROW'S SCHEDULE</Text>
            <Text style={styles.scheduleText}>Ready to plan your day ahead?</Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: { backgroundColor:'#04020a', flexGrow: 1 },
  container: { flex:1, backgroundColor:'#04020a', alignItems:'center', justifyContent:'center', padding:24, paddingVertical: 80 },
  label: { fontSize:10, color:'#7a6030', letterSpacing:3, marginBottom:24, textAlign:'center' },
  title: { fontSize:56, color:'#c9a84c', fontWeight:'bold', marginBottom:8, textAlign:'center' },
  subtitle: { fontSize:18, color:'#8a7e6a', textAlign:'center', marginBottom:48, lineHeight:28 },
  timeGreeting: { fontSize:20, color:'#c9a84c', fontWeight:'600', marginBottom:40, textAlign:'center', letterSpacing:1 },
  btn: { backgroundColor:'#c9a84c', padding:18, paddingHorizontal:40, borderRadius:2, marginBottom:16, width: '100%', alignItems:'center' },
  btnText: { color:'#04020a', fontWeight:'bold', letterSpacing:2, fontSize:13 },
  scheduleBox: { marginTop:40, padding:24, borderWidth:1, borderColor:'#7a6030', backgroundColor:'#0a0a0a' },
  scheduleTitle: { fontSize:14, color:'#c9a84c', fontWeight:'bold', letterSpacing:1, marginBottom:12 },
  scheduleText: { fontSize:13, color:'#8a7e6a', lineHeight:20 }
});