import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView } from 'react-native';
import { useState } from 'react';

export default function MorningScreen() {
  const [energy, setEnergy] = useState(0);
  const [intention, setIntention] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const energyLevels = ['💀 Dead', '😴 Low', '😐 Okay', '⚡ Good', '🔥 Elite'];

  return (
    <ScrollView style={styles.scroll}>
      <View style={styles.container}>
        <Text style={styles.label}>✦ MORNING CHECK-IN ✦</Text>
        <Text style={styles.title}>How are you{'\n'}showing up today?</Text>

        <Text style={styles.sectionLabel}>ENERGY LEVEL</Text>
        <View style={styles.energyRow}>
          {energyLevels.map((e, i) => (
            <TouchableOpacity
              key={i}
              style={[styles.energyBtn, energy === i+1 && styles.energySelected]}
              onPress={() => setEnergy(i+1)}>
              <Text style={styles.energyText}>{e}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.sectionLabel}>TODAY'S INTENTION</Text>
        <TextInput
          style={[styles.input, { color: '#f5f0e8' }]}
          placeholder="What will you accomplish today?"
          placeholderTextColor="#4a4030"
          multiline
          value={intention}
          onChangeText={setIntention}
        />

        <TouchableOpacity 
          style={[styles.btn, (!energy || !intention) && styles.btnDisabled]}
          onPress={() => setSubmitted(true)}
          disabled={!energy || !intention}>
          <Text style={styles.btnText}>SUBMIT TO JANANI</Text>
        </TouchableOpacity>

        {submitted && (
          <View style={styles.response}>
            <Text style={styles.responseText}>✦ Janani has received your morning. She is watching. ✦</Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: { backgroundColor:'#04020a' },
  container: { flex:1, padding:24, paddingTop:80 },
  label: { fontSize:10, color:'#7a6030', letterSpacing:3, marginBottom:24, textAlign:'center' },
  title: { fontSize:36, color:'#c9a84c', fontWeight:'bold', marginBottom:48, lineHeight:44 },
  sectionLabel: { fontSize:10, color:'#7a6030', letterSpacing:3, marginBottom:16 },
  energyRow: { flexDirection:'row', flexWrap:'wrap', gap:8, marginBottom:40 },
  energyBtn: { padding:10, paddingHorizontal:14, borderWidth:1, borderColor:'#3a2a10' },
  energySelected: { backgroundColor:'#c9a84c', borderColor:'#c9a84c' },
  energyText: { color:'#f5f0e8', fontSize:13 },
  input: { borderWidth:1, borderColor:'#3a2a10', padding:16, minHeight:120, marginBottom:40, fontSize:16, lineHeight:24 },
  btn: { backgroundColor:'#c9a84c', padding:18, alignItems:'center' },
  btnDisabled: { backgroundColor:'#3a2a10' },
  btnText: { color:'#04020a', fontWeight:'bold', letterSpacing:2 },
  response: { marginTop:32, padding:24, borderWidth:1, borderColor:'#7a6030' },
  responseText: { color:'#c9a84c', textAlign:'center', lineHeight:24, fontStyle:'italic' }
});