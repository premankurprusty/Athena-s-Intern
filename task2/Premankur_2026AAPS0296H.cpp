#include <Adafruit_LiquidCrystal.h>

// creating an enum of all possible states
enum class state {
	opensea,
 	anchored,
  	storm,
  	chardybis,
  	wrecked
};

//declaring the function to update the LCD and setting up initial conditions and variables.
void updateLCD(state current_state);
state current_state = state::opensea;
Adafruit_LiquidCrystal lcd(0);

void setup() {
  	lcd.begin(16, 2);
  	lcd.setBacklight(HIGH);

  	pinMode(0, INPUT_PULLUP); //button
  	pinMode(12, OUTPUT); //LED
  	pinMode(13, OUTPUT); //Buzzer
  	pinMode(1, OUTPUT); //Trig
  	pinMode(2, INPUT); //Echo
    updateLCD(current_state);
}

unsigned long timer;
bool anchorDropped = false;
int lastButtonState = HIGH;

// defining LCD updating logic
void updateLCD(state current_state) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("STATUS:");

    lcd.setCursor(0, 1);

    switch (current_state) {
        case state::opensea:
            lcd.print("OPEN SEA");
            break;

        case state::anchored:
            lcd.print("ANCHOR DROPPED");
            break;

        case state::storm:
            lcd.print("STORM");
            break;

         case state::chardybis:
            lcd.print("CHARYBDIS");
            break;

        case state::wrecked:
            lcd.print("WRECKED");
            break;
    }
}

// main loop
void loop() {
	// reading brightness level
    int brightness = analogRead(A0);

	// reading distance data
	digitalWrite(1, LOW);
	delayMicroseconds(2);
    digitalWrite(1, HIGH);
    delayMicroseconds(10);
    digitalWrite(1, LOW);
    long duration = pulseIn(2, HIGH);
    float distance = duration*0.0343/2.0;

	// reading button
    int buttonState = digitalRead(0);

	// checking if button is pressed and chnging anchor state
    if (lastButtonState == HIGH && buttonState == LOW) {
        anchorDropped = !anchorDropped;
    }

    lastButtonState = buttonState;

	// handling all the possible states (937 for brightness was from observation)
    switch (current_state) {
        case state::opensea:
            if (anchorDropped) {
                current_state = state::anchored;
                updateLCD(current_state);
            } 
			
			else if (brightness < 937) {
                current_state = state::storm;
                timer = millis();
                updateLCD(current_state);
            } 
			
			else if (distance < 100) {
                current_state = state::chardybis;
                timer = millis();
                updateLCD(current_state);
            }
            break;

        case state::anchored:
            if (!anchorDropped) {
                if (brightness < 937) {
                    current_state = state::storm;
                    timer = millis();
                    updateLCD(current_state);
                } 
				
				else if (distance < 100) {
                    current_state = state::chardybis;
                    timer = millis();
                    updateLCD(current_state);
                } 
				
				else {
                    current_state = state::opensea;
                    updateLCD(current_state);
                }
            }
            break;

        case state::storm:
            if (anchorDropped) {
                current_state = state::anchored;
                updateLCD(current_state);
            } 
			
			else if (brightness >= 937) {
                current_state = state::opensea;
                updateLCD(current_state);
            } 
			
			else if (millis() - timer >= 5000) {
                current_state = state::wrecked;
                updateLCD(current_state);
            }
            break;

        case state::chardybis:
            if (anchorDropped) {
                current_state = state::anchored;
                updateLCD(current_state);
            } 
			
			else if (distance >= 100) {
                current_state = state::opensea;
                updateLCD(current_state);
            } 
			
			else if (millis() - timer >= 5000) {
                current_state = state::wrecked;
                updateLCD(current_state);
            }
            break;
    }

	// handling buzzer and LED blinking cases
    if (current_state == state::storm) {
        digitalWrite(12, (millis() / 250) % 2);
    } else {
        digitalWrite(12, LOW);
    }

    if (current_state == state::chardybis) {
        tone(13, 440);
    } else {
        noTone(13);
    }
}
