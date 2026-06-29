const int ECG_PIN = A0;
// wiring
const int LO_PLUS  = 10;
const int LO_MINUS = 11;
// Moving average filter size
const int NUM_SAMPLES = 5;
int samples[NUM_SAMPLES];
int index = 0;
long total = 0;
int lastValue = 0;
int disconnectCounter = 0;
const int DISCONNECT_THRESHOLD = 15;

void setup() {
  Serial.begin(9600);
  pinMode(LO_PLUS, INPUT);
  pinMode(LO_MINUS, INPUT);
  for (int i = 0; i < NUM_SAMPLES; i++) {
    samples[i] = 0;
  }
}

void loop() {
  bool disconnected =
    (digitalRead(LO_PLUS) == 1) ||
    (digitalRead(LO_MINUS) == 1);
  if (disconnected) {
    disconnectCounter++;
  } else {
    disconnectCounter = 0;
  }
  if (disconnectCounter > DISCONNECT_THRESHOLD) {
    Serial.println(0);
  }
  else {
    total = total - samples[index];
    samples[index] = analogRead(ECG_PIN);
    total = total + samples[index];
    index++;
    if (index >= NUM_SAMPLES) {
      index = 0;
    }
    int filteredValue = total / NUM_SAMPLES;
    int difference = abs(filteredValue - lastValue);
    // Large unstable jump
    if (difference > 80) {
      // Show abnormal spike
      Serial.println(700);
    }
    else {
      // Normal ECG
      Serial.println(filteredValue);
    }
    lastValue = filteredValue;
  }
  delay(8);
}
