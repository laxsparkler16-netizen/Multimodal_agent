# 🔧 Troubleshooting Voice Recognition

## Quick Checklist

Before troubleshooting, please check:

- [ ] Are you using **Chrome** or **Edge** browser? (Required for Web Speech API)
- [ ] Have you **allowed microphone access**?
- [ ] Is your **microphone working** in other apps?
- [ ] Do you have an **internet connection**? (Required for Web Speech API)
- [ ] Have you **refreshed the page** after updates?

## Common Issues & Solutions

### Issue 1: "Web Speech API not available"

**Symptoms:**
- Message says "Please use Chrome or Edge browser"
- Falls back to demo mode

**Solution:**
1. **Use Chrome or Edge browser**
   - Download Chrome: https://www.google.com/chrome/
   - Download Edge: https://www.microsoft.com/edge
2. **Refresh the page** (F5 or Ctrl+R)
3. Look for message: "🎤 Real speech recognition enabled!"

**Browsers that DON'T work:**
- ❌ Firefox
- ❌ Safari
- ❌ Opera (sometimes)
- ❌ Internet Explorer

### Issue 2: "Microphone permission denied"

**Symptoms:**
- Error: "Microphone access denied"
- Recording doesn't start

**Solution:**

**In Chrome:**
1. Click the **lock icon** (🔒) in address bar
2. Find "Microphone" setting
3. Change to "Allow"
4. **Refresh the page**

**In Edge:**
1. Click the **lock icon** (🔒) in address bar
2. Click "Permissions for this site"
3. Set Microphone to "Allow"
4. **Refresh the page**

**Alternative:**
1. Go to browser settings
2. Search for "microphone"
3. Add http://localhost:8080 to allowed sites

### Issue 3: "No speech detected"

**Symptoms:**
- Recording starts but no transcription appears
- Error: "No speech detected. Please try again."

**Solution:**
1. **Speak louder** - The microphone might not pick up quiet speech
2. **Speak closer to microphone**
3. **Reduce background noise**
4. **Check microphone is working:**
   - Windows: Settings → System → Sound → Test microphone
   - Mac: System Preferences → Sound → Input
5. **Try a different microphone** if available
6. **Speak immediately** after clicking "Start Recording"

### Issue 4: Recording starts but transcription is wrong

**Symptoms:**
- Transcription appears but it's incorrect
- Words are misunderstood

**Solution:**
1. **Speak clearly** - Enunciate your words
2. **Speak at normal pace** - Not too fast or slow
3. **Use correct language** - Make sure selected language matches what you're speaking
4. **Reduce background noise**
5. **Check confidence score** - Low confidence (<70%) means poor recognition
6. **Try again** - Speech recognition improves with retries

### Issue 5: "Network error"

**Symptoms:**
- Error: "Network error. Check your connection."
- Recording works but transcription fails

**Solution:**
1. **Check internet connection** - Web Speech API requires internet
2. **Disable VPN** if you're using one
3. **Check firewall** - Make sure it's not blocking Google services
4. **Try different network** - Switch to different WiFi or mobile data
5. **Refresh the page**

### Issue 6: Recording indicator doesn't appear

**Symptoms:**
- Click "Start Recording" but nothing happens
- No visual feedback

**Solution:**
1. **Open browser console** (F12)
2. Look for error messages in Console tab
3. **Check JavaScript errors**
4. **Refresh the page** (Ctrl+Shift+R for hard refresh)
5. **Clear browser cache**

### Issue 7: Works in English but not in other languages

**Symptoms:**
- English transcription works
- Hindi/Tamil/other languages don't work or are inaccurate

**Solution:**
1. **Verify language is supported:**
   - en-US ✅
   - hi-IN ✅
   - ta-IN ✅
   - te-IN ✅
   - kn-IN ✅
   - ml-IN ✅
   - bn-IN ✅
   - mr-IN ✅

2. **Speak clearly in that language**
3. **Check you selected correct language** in dropdown
4. **Some languages work better than others** - English typically has best accuracy
5. **Try speaking common phrases first** to test

## Debugging Steps

### Step 1: Check Browser Console

1. Press **F12** to open Developer Tools
2. Click **Console** tab
3. Look for messages:
   - ✅ "Web Speech API is supported!" - Good!
   - ❌ "Web Speech API not supported" - Use Chrome/Edge
   - 🎤 "Speech recognition started" - Recording started
   - ✅ "Transcription: [your text]" - Success!
   - ❌ Red error messages - Problem!

### Step 2: Test Microphone

1. Go to https://www.onlinemictest.com/
2. Click "Play test"
3. Speak into microphone
4. See if it picks up your voice
5. If not working there, fix microphone first

### Step 3: Test in Simple Page

1. Open new tab
2. Go to: https://www.google.com/
3. Click microphone icon in search box
4. Try voice search
5. If Google voice search works, our app should work too

### Step 4: Check Network

1. Open browser console (F12)
2. Click **Network** tab
3. Click "Start Recording" and speak
4. Look for network requests
5. Check if any requests fail

## Still Not Working?

### Collect Information:

Please provide:
1. **Browser name and version**
   - Chrome: Help → About Google Chrome
   - Edge: Help → About Microsoft Edge

2. **Operating System**
   - Windows 10/11?
   - Mac?
   - Linux?

3. **What happens when you click "Start Recording"?**
   - Nothing?
   - Error message?
   - Recording starts but no transcription?

4. **Console errors** (F12 → Console tab)
   - Copy any red error messages

5. **Selected language**
   - Which language did you select?
   - Which language did you speak?

### Alternative: Use Demo Mode

If Web Speech API doesn't work:
1. The app will automatically fall back to demo mode
2. You'll see demo transcriptions
3. All features still work for testing
4. Translation still works

## Browser-Specific Issues

### Chrome Issues

**Issue:** "This site has been blocked from accessing your microphone"
**Solution:**
1. Go to chrome://settings/content/microphone
2. Remove localhost from blocked list
3. Add to allowed list
4. Refresh page

### Edge Issues

**Issue:** Microphone permission keeps resetting
**Solution:**
1. Go to edge://settings/content/microphone
2. Add http://localhost:8080 to allowed
3. Restart Edge
4. Try again

### Windows Issues

**Issue:** Microphone works in other apps but not browser
**Solution:**
1. Windows Settings → Privacy → Microphone
2. Enable "Allow apps to access your microphone"
3. Enable "Allow desktop apps to access your microphone"
4. Restart browser

### Mac Issues

**Issue:** Browser can't access microphone
**Solution:**
1. System Preferences → Security & Privacy → Privacy
2. Click "Microphone" in left sidebar
3. Check the box next to Chrome/Edge
4. Restart browser

## Performance Tips

1. **Close other tabs** - Reduces browser load
2. **Close other apps** - Frees up system resources
3. **Use wired microphone** - Better quality than built-in
4. **Quiet environment** - Reduces background noise
5. **Speak naturally** - Don't shout or whisper

## Expected Behavior

### Correct Flow:
1. Select language → ✅ "Input language selected"
2. Click "Start Recording" → 🎤 "Listening... Speak now!"
3. Speak → Recording indicator pulses
4. Auto-stops or click "Stop" → Processing
5. Transcription appears → ✅ "Transcription complete! (Confidence: XX%)"

### What You Should See:
- Green success messages
- Transcription in text box
- Confidence score (70-100% is good)
- Translate button becomes enabled

## Contact Information

If none of these solutions work, please provide:
- Browser and version
- Operating system
- Console error messages (F12 → Console)
- What happens step-by-step

---

**Most common fix: Use Chrome or Edge browser and allow microphone access!** 🎤
