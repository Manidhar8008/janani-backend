import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>✦ PERSONAL INTELLIGENCE ENGINE ✦</Text>
      <Text style={styles.title}>Janani.AI</Text>
      <Text style={styles.subtitle}>She watches. She knows.{'\n'}She unlocks you.</Text>
      <TouchableOpacity style={styles.btn}>
        <Text style={styles.btnText}>BEGIN MORNING CHECK-IN</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex:1, backgroundColor:'#04020a', alignItems:'center', justifyContent:'center', padding:24 },
  label: { fontSize:10, color:'#7a6030', letterSpacing:3, marginBottom:24 },
  title: { fontSize:56, color:'#c9a84c', fontWeight:'bold', marginBottom:8 },
  subtitle: { fontSize:18, color:'#8a7e6a', textAlign:'center', marginBottom:64, lineHeight:28 },
  btn: { backgroundColor:'#c9a84c', padding:18, paddingHorizontal:40, borderRadius:2 },
  btnText: { color:'#04020a', fontWeight:'bold', letterSpacing:2, fontSize:13 }
});