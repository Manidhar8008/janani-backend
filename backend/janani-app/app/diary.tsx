import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView } from 'react-native';
import { useState } from 'react';
import { useRouter } from 'expo-router';

export default function DiaryScreen() {
  const router = useRouter();
  const [diaryEntry, setDiaryEntry] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [mood, setMood] = useState(0);

  const moods = ['😢 Sad', '😐 Neutral', '😊 Happy', '🤩 Excited', '🔥 Unstoppable'];

  return (
    <ScrollView style={styles.scroll}>
      <View style={styles.container}>
        <Text style={styles.label}>✦ DIARY UPDATE ✦</Text>
        <Text style={styles.title}>Reflect{'\n'}on your day</Text>

        <Text style={styles.sectionLabel}>YOUR MOOD</Text>
        <View style={styles.moodRow}>
          {moods.map((m, i) => (
            <TouchableOpacity
              key={i}
              style={[styles.moodBtn, mood === i+1 && styles.moodSelected]}
              onPress={() => setMood(i+1)}>
              <Text style={styles.moodText}>{m}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.sectionLabel}>TODAY'S REFLECTION</Text>
        <TextInput
          style={[styles.input, { color: '#f5f0e8' }]}
          placeholder="What happened today? What did you learn?"
          placeholderTextColor="#4a4030"
          multiline
          value={diaryEntry}
          onChangeText={setDiaryEntry}
        />

        <TouchableOpacity 
          style={[styles.btn, (!mood || !diaryEntry) && styles.btnDisabled]}
          onPress={() => setSubmitted(true)}
          disabled={!mood || !diaryEntry}>
          <Text style={styles.btnText}>SUBMIT TO JANANI</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.backBtn}
          onPress={() => router.back()}>
          <Text style={styles.backBtnText}>← BACK</Text>
        </TouchableOpacity>

        {submitted && (
          <View style={styles.response}>
            <Text style={styles.responseText}>✦ Janani has recorded your day. Your growth is noted. ✦</Text>
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
  moodRow: { flexDirection:'row', flexWrap:'wrap', gap:8, marginBottom:40 },
  moodBtn: { padding:10, paddingHorizontal:14, borderWidth:1, borderColor:'#3a2a10' },
  moodSelected: { backgroundColor:'#c9a84c', borderColor:'#c9a84c' },
  moodText: { color:'#f5f0e8', fontSize:13 },
  input: { borderWidth:1, borderColor:'#3a2a10', padding:16, minHeight:120, marginBottom:40, fontSize:16, lineHeight:24 },
  btn: { backgroundColor:'#c9a84c', padding:18, alignItems:'center', marginBottom:12 },
  btnDisabled: { backgroundColor:'#3a2a10' },
  btnText: { color:'#04020a', fontWeight:'bold', letterSpacing:2 },
  backBtn: { padding:12, alignItems:'center', borderWidth:1, borderColor:'#7a6030' },
  backBtnText: { color:'#8a7e6a', fontWeight:'600', letterSpacing:1 },
  response: { marginTop:32, padding:24, borderWidth:1, borderColor:'#7a6030' },
  responseText: { color:'#c9a84c', textAlign:'center', lineHeight:24, fontStyle:'italic' }
});
