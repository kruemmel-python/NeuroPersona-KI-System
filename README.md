# NeuroPersona

## **Einführung**

NeuroPersona ist ein einzigartiges KI-System, das auf den Prinzipien des menschlichen Gehirns basiert. Es simuliert kognitive Prozesse, um datengetriebene Entscheidungen zu treffen, Szenarien zu simulieren und kontextspezifische Informationen zu verarbeiten. Das System vereint mehrere spezialisierte Module – "Gehirne" –, die miteinander interagieren, um eine menschenähnliche Analyse- und Entscheidungsstruktur zu erzeugen.

Dieses Modell wurde mit einem Fokus auf Modularität, Flexibilität und Effizienz entwickelt, sodass es auf verschiedene Anwendungsbereiche wie Marktforschung, psychologische Diagnostik, Verhaltensanalyse und Szenariosimulation angepasst werden kann.

---

## **Hauptfunktionen**

- Verarbeitung und Speicherung von Daten in Kurz-, Mittel- und Langzeitgedächtnis.
- Simulation und Bewertung von Szenarien.
- Kreative Generierung neuer Ideen.
- Emotionale Gewichtung von Informationen und Entscheidungen.
- Optimierung des Systems basierend auf Metakognition.
- Integration sozialer Dynamiken in die Entscheidungsfindung.

---

## **Systemarchitektur**

NeuroPersona basiert auf einer modularen Struktur, die in mehrere spezialisierte Gehirnmodule unterteilt ist. Jedes Modul repräsentiert eine Funktionseinheit des Systems und übernimmt spezifische Aufgaben.

### **1. Cortex Creativus**
- **Aufgabe:** Kreative Ideengenerierung.
- **Beschreibung:** Dieses Modul nimmt Informationen aus anderen Gehirnen auf und entwickelt daraus neue, originelle Ideen oder Hypothesen.
- **Anwendungsbeispiel:** Entwicklung neuer Produktideen auf Basis von Konsumentendaten.

---

### **2. Simulatrix Neuralis**
- **Aufgabe:** Simulation von Szenarien.
- **Beschreibung:** Führt hypothetische Analysen („Was-wäre-wenn“-Szenarien) durch, um zukünftige Ergebnisse oder Auswirkungen vorherzusagen.
- **Anwendungsbeispiel:** Prognose, wie sich Änderungen in Produktpreisen auf das Kaufverhalten auswirken könnten.

---

### **3. Cortex Criticus**
- **Aufgabe:** Kritische Bewertung und Validierung von Ideen.
- **Beschreibung:** Bewertet die Ideen und Szenarien des Cortex Creativus anhand festgelegter Kriterien, um deren Durchführbarkeit und Relevanz zu überprüfen.
- **Anwendungsbeispiel:** Validierung, ob eine neue Marketingstrategie effektiv und umsetzbar ist.

---

### **4. Limbus Affektus**
- **Aufgabe:** Emotionale Gewichtung.
- **Beschreibung:** Simuliert die Rolle von Emotionen bei der Entscheidungsfindung, indem es Ideen und Konzepte basierend auf emotionalen Faktoren verstärkt oder abschwächt.
- **Anwendungsbeispiel:** Priorisierung nachhaltiger Optionen aufgrund ihrer emotionalen Resonanz bei Konsumenten.

---

### **5. Meta Cognitio**
- **Aufgabe:** Systemoptimierung.
- **Beschreibung:** Analysiert die Leistung des Systems und optimiert es durch Anpassung von Lernraten, Gewichtungen und Verbindungen, um Effizienz und Stabilität zu verbessern.
- **Anwendungsbeispiel:** Dynamische Anpassung der Lernrate, um Überaktivierung zu vermeiden.

---

### **6. Cortex Socialis**
- **Aufgabe:** Soziale Interaktion und Netzwerkeffekte.
- **Beschreibung:** Simuliert soziale Dynamiken und untersucht, wie externe Einflüsse, wie Gruppendruck, die Entscheidungen beeinflussen.
- **Anwendungsbeispiel:** Analyse, wie soziale Medien das Konsumverhalten beeinflussen.

---

### **7. Gedächtnisarchitektur**
NeuroPersona verfügt über eine dreistufige Gedächtnisarchitektur, die Informationen in Kurz-, Mittel- und Langzeitgedächtnis organisiert. Diese Ebenen ermöglichen eine realistische Modellierung von Vergessen, Lernen und Erinnern.

- **Kurzzeitgedächtnis:** Speichert Informationen für kurze Zeiträume und vergisst schnell.
- **Mittelfristiges Gedächtnis:** Übergangsstufe, in der wichtige Informationen länger behalten werden.
- **Langzeitgedächtnis:** Speichert relevante Informationen dauerhaft.

---

### **8. Kontextuelle Verarbeitung**
- Das System nutzt **kontextuelle Faktoren**, um die Relevanz von Informationen zu bewerten und deren Verarbeitung zu beeinflussen.
- Es integriert **emotionale Zustände** und **soziale Interaktionen**, um Entscheidungen anzupassen.

---

## **Funktionsweise**

1. **Dateneingabe:** Das System verarbeitet numerische, kategorische und textbasierte Daten.
2. **Verarbeitung durch Module:** Die Daten werden von verschiedenen Gehirnen analysiert und verarbeitet.
3. **Signalpropagation:** Informationen durchlaufen das neuronale Netzwerk und aktivieren relevante Module.
4. **Speicherung:** Relevante Informationen werden im Langzeitgedächtnis gespeichert, während irrelevante Daten vergessen werden.
5. **Ausgabe:** Das System liefert analysierte Ergebnisse, Empfehlungen oder Vorhersagen.

---

## **Technische Details**

- **Programmiersprache:** Python
- **Bibliotheken:**
  - `numpy` und `pandas` für Datenverarbeitung.
  - `matplotlib` und `plotly` für Visualisierungen.
  - `torch` für GPU-gestützte Berechnungen (optional).
  - `networkx` für Netzwerkanalyse.
  - `streamlit` für das Dashboard.

- **Optimierung:**
  - GPU-Beschleunigung kann aktiviert werden.
  - Dynamische Anpassung von Lern- und Decay-Raten.
  - Modularität ermöglicht Anpassungen an spezifische Anwendungsfälle.

---

## **Installation**

1. Klone das Repository:
   ```bash
   git clone https://github.com/kruemmel-python/NeuroPersona.git
   ```
2. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
3. Starte das Dashboard:
   ```bash
   streamlit run main.py
   ```

---

## **Visualisierungen**

### **1. Netzwerktopologie**
- Zeigt die Verbindungen zwischen den Modulen.
- Unterstützt 3D-Visualisierungen für eine intuitive Darstellung.

### **2. Aktivierungsverläufe**
- Diagramme zeigen, wie sich die Aktivierungen der Module über die Zeit entwickeln.

### **3. Gedächtnisverteilung**
- Balkendiagramme zeigen die Anzahl der Knoten in den Gedächtnisebenen (Kurz-, Mittel- und Langzeit).

### **4. Heatmaps**
- Veranschaulichen die Aktivierungswerte der Module über mehrere Epochen.

---

## **Beispiele für Anwendungsfälle**

- **Marktforschung:** Analyse von Umfragedaten und Erstellung neuer Produktideen.
- **Psychologische Diagnostik:** Simulation emotionaler Zustände und deren Einfluss auf Entscheidungen.
- **Bildungssektor:** Personalisierte Lernpfade basierend auf individuellen Präferenzen.
- **Gesundheitswesen:** Einblicke in Patientenverhalten und Präferenzen.
- **Wirtschaft:** Vorhersage von Markttrends und Risikomanagement.

---

## **Zukunftsperspektiven**

- **Erweiterte Visualisierungen:** Implementierung zusätzlicher Dashboards für tiefere Einblicke.
- **Multimodale Datenintegration:** Erweiterung um Bild- und Audiodaten.
- **Echtzeitverarbeitung:** Integration von Live-Daten für kontinuierliche Analyse.

---

## **Kontakt**

Für Fragen oder Vorschläge:  
**Entwickler:** Ralf Krümmel  
**E-Mail:** support@ciphercore.de  
**GitHub:** kruemmel-python

