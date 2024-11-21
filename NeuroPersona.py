import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm  # Für Fortschrittsbalken
import tkinter as tk
from tkinter import ttk
import seaborn as sns
import networkx as nx
import json
import os
import time
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
import torch

# --- Debugging-Funktion ---
def debug_connections(category_nodes):
    start_time = time.time()
    """
    Gibt die Verbindungen und Gewichte aller Knoten aus.

    Diese Funktion durchläuft alle Knoten und deren Verbindungen und druckt die Verbindungen und deren Gewichte.
    Dies ist nützlich für das Debugging, um sicherzustellen, dass die Verbindungen korrekt initialisiert wurden.

    Args:
        category_nodes (list): Eine Liste von Knotenobjekten.
    """
    for node in category_nodes:
        print(f"Knoten: {node.label}")
        for conn in node.connections:
            print(f"  Verbindung zu: {conn.target_node.label}, Gewicht: {conn.weight}")
    end_time = time.time()
    print(f"debug_connections Ausführungszeit: {end_time - start_time:.4f} Sekunden")

# --- Hilfsfunktionen ---
def sigmoid(x):
    start_time = time.time()
    """
    Sigmoid-Aktivierungsfunktion.

    Die Sigmoid-Funktion wird verwendet, um die Aktivierung eines Knotens zu berechnen.
    Sie mappt Eingabewerte auf den Bereich [0, 1].

    Args:
        x (float): Eingabewert.

    Returns:
        float: Aktivierungswert im Bereich [0, 1].
    """
    result = 1 / (1 + np.exp(-x))
    end_time = time.time()
    print(f"sigmoid Ausführungszeit: {end_time - start_time:.4f} Sekunden")
    return result

def add_activation_noise(activation, noise_level=0.1):
    start_time = time.time()
    """
    Fügt der Aktivierung Rauschen hinzu, um menschliche Variabilität zu simulieren.

    Diese Funktion fügt normalverteiltes Rauschen zur Aktivierung hinzu, um die Variabilität zu erhöhen.
    Der resultierende Wert wird auf den Bereich [0, 1] begrenzt.

    Args:
        activation (float): Aktivierungswert.
        noise_level (float): Standardabweichung des Rauschens.

    Returns:
        float: Aktivierungswert mit Rauschen.
    """
    noise = np.random.normal(0, noise_level)
    result = np.clip(activation + noise, 0.0, 1.0)
    end_time = time.time()
    print(f"add_activation_noise Ausführungszeit: {end_time - start_time:.4f} Sekunden")
    return result

def decay_weights(category_nodes, decay_rate=0.002, forgetting_curve=0.95):
    start_time = time.time()
    """
    Schwächt die Verbindungsgewichte exponentiell, um das Vergessen zu simulieren.

    Diese Funktion reduziert die Gewichte der Verbindungen zwischen den Knoten, um das Vergessen zu simulieren.
    Die Reduktion erfolgt exponentiell basierend auf der Vergessenskurve.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        decay_rate (float): Rate, mit der die Gewichte abnehmen.
        forgetting_curve (float): Faktor, der die Vergessenskurve bestimmt.
    """
    for node in category_nodes:
        for conn in node.connections:
            conn.weight *= (1 - decay_rate) * forgetting_curve
    end_time = time.time()
    print(f"decay_weights Ausführungszeit: {end_time - start_time:.4f} Sekunden")

def reward_connections(category_nodes, target_category, reward_factor=0.1):
    start_time = time.time()
    """
    Belohnt Verbindungen zu einem bestimmten Zielknoten.

    Diese Funktion erhöht die Gewichte der Verbindungen zu einem bestimmten Zielknoten, um Belohnungen zu simulieren.
    Die Gewichte werden auf den Bereich [0, 1] begrenzt.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        target_category (str): Label des Zielknotens.
        reward_factor (float): Faktor, um den die Gewichte erhöht werden.
    """
    for node in category_nodes:
        if node.label == target_category:
            for conn in node.connections:
                conn.weight += reward_factor
                conn.weight = np.clip(conn.weight, 0, 1.0)
    end_time = time.time()
    print(f"reward_connections Ausführungszeit: {end_time - start_time:.4f} Sekunden")

def apply_emotion_weight(activation, category_label, emotion_weights, emotional_state=1.0):
    start_time = time.time()
    """
    Modifiziert die Aktivierung basierend auf einer emotionalen Gewichtung und dem aktuellen emotionalen Zustand.

    Diese Funktion passt die Aktivierung eines Knotens basierend auf einer emotionalen Gewichtung und dem aktuellen emotionalen Zustand an.
    Dies simuliert den Einfluss von Emotionen auf die Aktivierung.

    Args:
        activation (float): Aktivierungswert.
        category_label (str): Label der Kategorie.
        emotion_weights (dict): Dictionary mit emotionalen Gewichtungen.
        emotional_state (float): Aktueller emotionaler Zustand.

    Returns:
        float: Angepasster Aktivierungswert.
    """
    emotion_factor = emotion_weights.get(category_label, 1.0) * emotional_state
    result = activation * emotion_factor
    end_time = time.time()
    print(f"apply_emotion_weight Ausführungszeit: {end_time - start_time:.4f} Sekunden")
    return result

def generate_simulated_answers(data, personality_distributions):
    start_time = time.time()
    """
    Generiert simulierte Antworten basierend auf Persönlichkeitsverteilungen.

    Diese Funktion generiert simulierte Antworten basierend auf den Persönlichkeitsverteilungen der Kategorien.
    Die Antworten werden normalverteilt um den Mittelwert der Persönlichkeitsverteilung erzeugt und auf den Bereich [0, 1] begrenzt.

    Args:
        data (pd.DataFrame): DataFrame mit den Daten.
        personality_distributions (dict): Dictionary mit Persönlichkeitsverteilungen.

    Returns:
        list: Liste der simulierten Antworten.
    """
    simulated_answers = []
    for _, row in data.iterrows():
        category = row['Kategorie']
        mean = personality_distributions.get(category, 0.5)
        simulated_answer = np.clip(np.random.normal(mean, 0.2), 0.0, 1.0)
        simulated_answers.append(simulated_answer)
    end_time = time.time()
    print(f"generate_simulated_answers Ausführungszeit: {end_time - start_time:.4f} Sekunden")
    return simulated_answers

def social_influence(category_nodes, social_network, influence_factor=0.1):
    start_time = time.time()
    """
    Simuliert den Einfluss sozialer Interaktionen auf die Verbindungsgewichte.

    Diese Funktion passt die Gewichte der Verbindungen basierend auf sozialen Interaktionen an.
    Der Einfluss wird durch den Einflussfaktor und die sozialen Netzwerkgewichte bestimmt.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        social_network (dict): Dictionary mit sozialen Netzwerkgewichten.
        influence_factor (float): Faktor, der den Einfluss bestimmt.
    """
    for node in category_nodes:
        for conn in node.connections:
            social_impact = sum([social_network.get(conn.target_node.label, 0)]) * influence_factor
            conn.weight += social_impact
            conn.weight = np.clip(conn.weight, 0, 1.0)
    end_time = time.time()
    print(f"social_influence Ausführungszeit: {end_time - start_time:.4f} Sekunden")

def update_emotional_state(emotional_state, emotional_change_rate=0.02):
    start_time = time.time()
    """
    Aktualisiert den emotionalen Zustand basierend auf einer Änderungsrate.

    Diese Funktion aktualisiert den emotionalen Zustand basierend auf einer Änderungsrate.
    Der emotionale Zustand wird auf den Bereich [0.7, 1.5] begrenzt.

    Args:
        emotional_state (float): Aktueller emotionaler Zustand.
        emotional_change_rate (float): Rate der emotionalen Änderung.

    Returns:
        float: Aktualisierter emotionaler Zustand.
    """
    emotional_state += np.random.normal(0, emotional_change_rate)
    result = np.clip(emotional_state, 0.7, 1.5)
    end_time = time.time()
    print(f"update_emotional_state Ausführungszeit: {end_time - start_time:.4f} Sekunden")
    return result

def apply_contextual_factors(activation, node, context_factors):
    start_time = time.time()
    """
    Modifiziert die Aktivierung basierend auf kontextuellen Faktoren.

    Diese Funktion passt die Aktivierung eines Knotens basierend auf kontextuellen Faktoren an.
    Dies simuliert den Einfluss von Kontext auf die Aktivierung.

    Args:
        activation (float): Aktivierungswert.
        node (Node): Knotenobjekt.
        context_factors (dict): Dictionary mit kontextuellen Faktoren.

    Returns:
        float: Angepasster Aktivierungswert.
    """
    context_factor = context_factors.get(node.label, 1.0)
    result = activation * context_factor * random.uniform(0.9, 1.1)
    end_time = time.time()
    print(f"apply_contextual_factors Ausführungszeit: {end_time - start_time:.4f} Sekunden")
    return result

def long_term_memory(category_nodes, long_term_factor=0.01):
    start_time = time.time()
    """
    Simuliert langfristige Gewichtsanpassungen für das Langzeitgedächtnis.

    Diese Funktion passt die Gewichte der Verbindungen langfristig an, um das Langzeitgedächtnis zu simulieren.
    Die Gewichte werden auf den Bereich [0, 1] begrenzt.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        long_term_factor (float): Faktor für langfristige Anpassungen.
    """
    for node in category_nodes:
        for conn in node.connections:
            conn.weight += long_term_factor * conn.weight
            conn.weight = np.clip(conn.weight, 0, 1.0)
    end_time = time.time()
    print(f"long_term_memory Ausführungszeit: {end_time - start_time:.4f} Sekunden")

def hebbian_learning(node, learning_rate=0.3, weight_limit=1.0, reg_factor=0.005):
    start_time = time.time()
    """
    Hebb'sches Lernen mit Begrenzung und Regularisierung.

    Diese Funktion implementiert Hebb'sches Lernen, bei dem die Gewichte der Verbindungen basierend auf der Aktivierung der Knoten angepasst werden.
    Die Gewichte werden auf den Bereich [-weight_limit, weight_limit] begrenzt und eine Regularisierung wird angewendet.

    Args:
        node (Node): Knotenobjekt.
        learning_rate (float): Lernrate.
        weight_limit (float): Begrenzung der Gewichte.
        reg_factor (float): Regularisierungsfaktor.
    """
    for connection in node.connections:
        old_weight = connection.weight
        connection.weight += learning_rate * node.activation * connection.target_node.activation
        connection.weight = np.clip(connection.weight, -weight_limit, weight_limit)
        connection.weight -= reg_factor * connection.weight
        print(f"Gewicht {old_weight:.4f} -> {connection.weight:.4f}")
    end_time = time.time()
    print(f"hebbian_learning Ausführungszeit: {end_time - start_time:.4f} Sekunden")

# --- Klassen für Netzwerkstruktur ---
class Connection:
    """
    Klasse für Verbindungen zwischen Knoten.

    Diese Klasse repräsentiert eine Verbindung zwischen zwei Knoten mit einem Gewicht.

    Attributes:
        target_node (Node): Zielknoten der Verbindung.
        weight (float): Gewicht der Verbindung.
    """
    def __init__(self, target_node, weight=None):
        self.target_node = target_node
        self.weight = weight if weight is not None else random.uniform(0.1, 1.0)

class Node:
    """
    Klasse für Knoten im Netzwerk.

    Diese Klasse repräsentiert einen Knoten im Netzwerk mit einem Label, Verbindungen und einem Aktivierungswert.

    Attributes:
        label (str): Label des Knotens.
        connections (list): Liste von Verbindungen.
        activation (float): Aktivierungswert.
    """
    def __init__(self, label):
        self.label = label
        self.connections = []
        self.activation = 0.0

    def add_connection(self, target_node, weight=None):
        """
        Fügt eine Verbindung zu einem Zielknoten hinzu.

        Args:
            target_node (Node): Zielknoten der Verbindung.
            weight (float): Gewicht der Verbindung.
        """
        self.connections.append(Connection(target_node, weight))

class MemoryNode(Node):
    """
    Erweitert Node, um verschiedene Gedächtnisebenen zu simulieren.

    Diese Klasse erweitert die Node-Klasse, um verschiedene Gedächtnisebenen zu simulieren.

    Attributes:
        memory_type (str): Gedächtnistyp ('short_term', 'mid_term', 'long_term').
        retention_time (int): Zeit, die die Information in dieser Stufe verbracht hat.
        activation_history (list): Historie der Aktivierungen.
    """
    def __init__(self, label, memory_type="short_term"):
        super().__init__(label)
        self.memory_type = memory_type
        self.retention_time = {"short_term": 5, "mid_term": 20, "long_term": 100}[memory_type]
        self.time_in_memory = 0
        self.activation_history = []

    def decay(self, decay_rate, context_factors, emotional_state):
        """
        Schwächt Verbindungen, abhängig vom Gedächtnistyp, Kontextfaktoren und emotionalem Zustand.

        Diese Funktion reduziert die Gewichte der Verbindungen basierend auf dem Gedächtnistyp, Kontextfaktoren und emotionalem Zustand.

        Args:
            decay_rate (float): Rate, mit der die Gewichte abnehmen.
            context_factors (dict): Dictionary mit kontextuellen Faktoren.
            emotional_state (float): Aktueller emotionaler Zustand.
        """
        context_factor = context_factors.get(self.label, 1.0)
        emotional_factor = emotional_state
        for conn in self.connections:
            if self.memory_type == "short_term":
                conn.weight *= (1 - decay_rate * 2 * context_factor * emotional_factor)
            elif self.memory_type == "mid_term":
                conn.weight *= (1 - decay_rate * context_factor * emotional_factor)
            elif self.memory_type == "long_term":
                conn.weight *= (1 - decay_rate * 0.5 * context_factor * emotional_factor)

    def promote(self, activation_threshold=0.7):
        """
        Wechselt die Information zur nächsten Gedächtnisstufe basierend auf Aktivierung und sozialen Interaktionen.

        Diese Funktion wechselt die Information zur nächsten Gedächtnisstufe, wenn die durchschnittliche Aktivierung einen Schwellenwert überschreitet.

        Args:
            activation_threshold (float): Schwellenwert für die Aktivierung.
        """
        if len(self.activation_history) == 0:
            return
        if self.memory_type == "short_term" and np.mean(self.activation_history[-5:]) > activation_threshold:
            self.memory_type = "mid_term"
            self.retention_time = 20
        elif self.memory_type == "mid_term" and np.mean(self.activation_history[-20:]) > activation_threshold:
            self.memory_type = "long_term"
            self.retention_time = 100

class CortexCreativus(Node):
    def __init__(self, label):
        super().__init__(label)

    def generate_new_ideas(self, category_nodes):
        """
        Generiert neue Ideen basierend auf den Aktivierungen der Knoten im Netzwerk.

        Args:
            category_nodes (list): Liste von Knotenobjekten.

        Returns:
            list: Liste neuer Ideen.
        """
        new_ideas = []
        for node in category_nodes:
            if node.activation > 0.5:  # Beispielschwellenwert für Aktivierung
                new_idea = f"New idea based on {node.label} with activation {node.activation}"
                new_ideas.append(new_idea)
        return new_ideas

class SimulatrixNeuralis(Node):
    def __init__(self, label):
        super().__init__(label)

    def simulate_scenarios(self, category_nodes):
        """
        Simuliert Szenarien basierend auf den Aktivierungen der Knoten im Netzwerk.

        Args:
            category_nodes (list): Liste von Knotenobjekten.

        Returns:
            list: Liste simulierter Szenarien.
        """
        scenarios = []
        for node in category_nodes:
            if node.activation > 0.5:  # Beispielschwellenwert für Aktivierung
                scenario = f"Simulated scenario based on {node.label} with activation {node.activation}"
                scenarios.append(scenario)
        return scenarios

class CortexCriticus(Node):
    def __init__(self, label):
        super().__init__(label)

    def evaluate_ideas(self, ideas):
        """
        Bewertet Ideen basierend auf bestimmten Kriterien.

        Args:
            ideas (list): Liste von Ideen.

        Returns:
            list: Liste bewerteter Ideen.
        """
        evaluated_ideas = []
        for idea in ideas:
            evaluation_score = random.uniform(0, 1)  # Beispielbewertung
            evaluation = f"Evaluated idea: {idea} - Score: {evaluation_score}"
            evaluated_ideas.append(evaluation)
        return evaluated_ideas

class LimbusAffektus(Node):
    def __init__(self, label):
        super().__init__(label)

    def apply_emotional_weight(self, ideas, emotional_state):
        """
        Wendet emotionale Gewichtung auf Ideen an.

        Args:
            ideas (list): Liste von Ideen.
            emotional_state (float): Emotionaler Zustand.

        Returns:
            list: Liste emotional gewichteter Ideen.
        """
        weighted_ideas = []
        for idea in ideas:
            weighted_idea = f"Emotionally weighted idea: {idea} - Weight: {emotional_state}"
            weighted_ideas.append(weighted_idea)
        return weighted_ideas

class MetaCognitio(Node):
    def __init__(self, label):
        super().__init__(label)

    def optimize_system(self, category_nodes):
        """
        Optimiert das System basierend auf Metakognition.

        Args:
            category_nodes (list): Liste von Knotenobjekten.
        """
        for node in category_nodes:
            node.activation *= random.uniform(0.9, 1.1)  # Beispieloptimierung

class CortexSocialis(Node):
    def __init__(self, label):
        super().__init__(label)

    def simulate_social_interactions(self, category_nodes):
        """
        Simuliert soziale Interaktionen basierend auf den Aktivierungen der Knoten im Netzwerk.

        Args:
            category_nodes (list): Liste von Knotenobjekten.

        Returns:
            list: Liste simulierter sozialer Interaktionen.
        """
        interactions = []
        for node in category_nodes:
            if node.activation > 0.5:  # Beispielschwellenwert für Aktivierung
                interaction = f"Simulated social interaction based on {node.label} with activation {node.activation}"
                interactions.append(interaction)
        return interactions

def connect_new_brains_to_network(category_nodes, new_brains):
    """
    Stellt Verbindungen zwischen den neuen Gehirnmodulen und den bestehenden Knoten her.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        new_brains (list): Liste der neuen Gehirnmodule.
    """
    for brain in new_brains:
        for node in category_nodes:
            brain.add_connection(node)
            node.add_connection(brain)

# --- Netzwerk-Initialisierung ---
def initialize_quiz_network(categories):
    """
    Erstellt ein Netzwerk mit Kategorien als Zielknoten.

    Diese Funktion initialisiert ein Netzwerk mit Kategorien als Zielknoten und verbindet alle Knoten miteinander.

    Args:
        categories (list): Liste von Kategorien.

    Returns:
        list: Liste von Knotenobjekten.
    """
    category_nodes = [Node(c) for c in categories]
    for node in category_nodes:
        for target_node in category_nodes:
            if node != target_node:
                node.add_connection(target_node)

    for node in category_nodes:
        if not hasattr(node, "activation_history"):
            node.activation_history = []

    debug_connections(category_nodes)
    return category_nodes

# --- Signalpropagation ---
def propagate_signal(node, input_signal, emotion_weights, emotional_state=1.0, context_factors=None):
    """
    Propagiert ein Signal durch das Netzwerk.

    Diese Funktion propagiert ein Signal durch das Netzwerk, indem sie die Aktivierung eines Knotens berechnet und an seine Verbindungen weitergibt.

    Args:
        node (Node): Knotenobjekt.
        input_signal (float): Eingabesignal.
        emotion_weights (dict): Dictionary mit emotionalen Gewichtungen.
        emotional_state (float): Aktueller emotionaler Zustand.
        context_factors (dict): Dictionary mit kontextuellen Faktoren.
    """
    node.activation = add_activation_noise(sigmoid(input_signal * random.uniform(0.8, 1.2)))
    node.activation = apply_emotion_weight(node.activation, node.label, emotion_weights, emotional_state)
    if context_factors:
        node.activation = apply_contextual_factors(node.activation, node, context_factors)
    print(f"Knoten {node.label}: Aktivierung {node.activation:.4f}")
    for connection in node.connections:
        connection.target_node.activation += node.activation * connection.weight

def propagate_signal_with_memory(node, input_signal, category_nodes, memory_nodes, context_factors, emotional_state):
    """
    Propagiert Signale und verwaltet den Übergang zwischen Gedächtnisstufen.

    Diese Funktion propagiert Signale durch das Netzwerk und verwaltet den Übergang zwischen Gedächtnisstufen.

    Args:
        node (Node): Knotenobjekt.
        input_signal (float): Eingabesignal.
        category_nodes (list): Liste von Knotenobjekten.
        memory_nodes (list): Liste von Gedächtnisknoten.
        context_factors (dict): Dictionary mit kontextuellen Faktoren.
        emotional_state (float): Aktueller emotionaler Zustand.
    """
    node.activation = add_activation_noise(sigmoid(input_signal))
    node.activation_history.append(node.activation)
    for connection in node.connections:
        connection.target_node.activation += node.activation * connection.weight

    for memory_node in memory_nodes:
        memory_node.time_in_memory += 1
        memory_node.promote()

# --- Simulation mit Anpassungen ---
def simulate_learning(data, category_nodes, personality_distributions, epochs=100, learning_rate=0.8, reward_interval=5, decay_rate=0.002, emotional_state=1.0, context_factors=None):
    """
    Simuliert das Lernen im Netzwerk.

    Diese Funktion simuliert das Lernen im Netzwerk über mehrere Epochen hinweg.
    Sie aktualisiert die Gewichte der Verbindungen basierend auf verschiedenen Faktoren und visualisiert die Ergebnisse.

    Args:
        data (pd.DataFrame): DataFrame mit den Daten.
        category_nodes (list): Liste von Knotenobjekten.
        personality_distributions (dict): Dictionary mit Persönlichkeitsverteilungen.
        epochs (int): Anzahl der Epochen.
        learning_rate (float): Lernrate.
        reward_interval (int): Intervall für Belohnungen.
        decay_rate (float): Rate, mit der die Gewichte abnehmen.
        emotional_state (float): Aktueller emotionaler Zustand.
        context_factors (dict): Dictionary mit kontextuellen Faktoren.

    Returns:
        tuple: Aktivierungsverlauf und Gewichtsverlauf.
    """
    if context_factors is None:
        context_factors = {}

    weights_history = {f"{node.label} → {conn.target_node.label}": [] for node in category_nodes for conn in node.connections}
    activation_history = {node.label: [] for node in category_nodes}

    question_nodes = []
    for idx, row in data.iterrows():
        q_node = Node(row['Frage'])
        question_nodes.append(q_node)
        category_label = row['Kategorie'].strip()
        category_node = next((c for c in category_nodes if c.label == category_label), None)
        if category_node:
            q_node.add_connection(category_node)
        else:
            print(f"Warnung: Kategorie '{category_label}' nicht gefunden für Frage '{row['Frage']}'.")

    emotion_weights = {category: 1.0 for category in data['Kategorie'].unique()}
    social_network = {category: random.uniform(0.1, 1.0) for category in data['Kategorie'].unique()}

    for epoch in range(epochs):
        print(f"\n--- Epoche {epoch + 1} ---")
        simulated_answers = generate_simulated_answers(data, personality_distributions)

        for node in category_nodes:
            node.activation_sum = 0.0
            node.activation_count = 0

        for idx, q_node in enumerate(question_nodes):
            for node in category_nodes + question_nodes:
                node.activation = 0.0

            answer = simulated_answers[idx]
            propagate_signal(q_node, answer, emotion_weights, emotional_state, context_factors)
            hebbian_learning(q_node, learning_rate)

            for node in category_nodes:
                node.activation_sum += node.activation
                if node.activation > 0:
                    node.activation_count += 1

            for node in category_nodes:
                for conn in node.connections:
                    weights_history[f"{node.label} → {conn.target_node.label}"].append(conn.weight)

        for node in category_nodes:
            if node.activation_count > 0:
                mean_activation = node.activation_sum / node.activation_count
                activation_history[node.label].append(mean_activation)
                print(f"Durchschnittliche Aktivierung für Knoten {node.label}: {mean_activation:.4f}")
            else:
                activation_history[node.label].append(0.0)
                print(f"Knoten {node.label} wurde in dieser Epoche nicht aktiviert.")

        if (epoch + 1) % reward_interval == 0:
            target_category = random.choice(data['Kategorie'].unique())
            reward_connections(category_nodes, target_category=target_category)

        decay_weights(category_nodes, decay_rate=decay_rate)
        social_influence(category_nodes, social_network)

    return activation_history, weights_history

def simulate_multilevel_memory(data, category_nodes, personality_distributions, epochs=100):
    """
    Simulation mit drei Gedächtnisstufen.

    Diese Funktion simuliert das Lernen im Netzwerk mit drei Gedächtnisstufen (kurzfristig, mittelfristig, langfristig).

    Args:
        data (pd.DataFrame): DataFrame mit den Daten.
        category_nodes (list): Liste von Knotenobjekten.
        personality_distributions (dict): Dictionary mit Persönlichkeitsverteilungen.
        epochs (int): Anzahl der Epochen.

    Returns:
        tuple: Kurzfristige, mittelfristige und langfristige Gedächtnisknoten.
    """
    short_term_memory = [MemoryNode(c, "short_term") for c in category_nodes]
    mid_term_memory = []
    long_term_memory = []
    memory_nodes = short_term_memory + mid_term_memory + long_term_memory
    context_factors = {question: random.uniform(0.9, 1.1) for question in data['Frage'].unique()}
    emotional_state = 1.0

    for epoch in range(epochs):
        print(f"\n--- Epoche {epoch + 1} ---")
        for node in short_term_memory:
            input_signal = random.uniform(0.1, 1.0)
            propagate_signal_with_memory(node, input_signal, category_nodes, memory_nodes, context_factors, emotional_state)

        for memory_node in memory_nodes:
            memory_node.decay(decay_rate=0.01, context_factors=context_factors, emotional_state=emotional_state)

        for memory_node in memory_nodes:
            memory_node.promote()

        short_term_memory, mid_term_memory, long_term_memory = update_memory_stages(memory_nodes)

    return short_term_memory, mid_term_memory, long_term_memory

def update_memory_stages(memory_nodes):
    """
    Aktualisiert die Gedächtnisstufen basierend auf den Gedächtnistypen.

    Diese Funktion aktualisiert die Gedächtnisstufen basierend auf den Gedächtnistypen der Knoten.

    Args:
        memory_nodes (list): Liste von Gedächtnisknoten.

    Returns:
        tuple: Kurzfristige, mittelfristige und langfristige Gedächtnisknoten.
    """
    short_term_memory = [node for node in memory_nodes if node.memory_type == "short_term"]
    mid_term_memory = [node for node in memory_nodes if node.memory_type == "mid_term"]
    long_term_memory = [node for node in memory_nodes if node.memory_type == "long_term"]
    return short_term_memory, mid_term_memory, long_term_memory

# --- Visualisierung der Aktivierungsentwicklung ---
def plot_activation_history(activation_history):
    """
    Visualisiert die Entwicklung der Aktivierungen über die Epochen.

    Diese Funktion visualisiert die Entwicklung der Aktivierungen über die Epochen.

    Args:
        activation_history (dict): Dictionary mit Aktivierungsverläufen.
    """
    plt.figure(figsize=(12, 8))
    for label, activations in activation_history.items():
        if len(activations) > 0:
            plt.plot(range(1, len(activations) + 1), activations, label=label)

    plt.title("Entwicklung der Aktivierungen während des Lernens")
    plt.xlabel("Epoche")
    plt.ylabel("Aktivierung")
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Visualisierung der Aktivierungs- und Gewichtsentwicklung ---
def plot_activation_and_weights(activation_history, weights_history):
    """
    Erstellt zwei Diagramme:
    1. Entwicklung der Aktivierungen über die Epochen.
    2. Entwicklung der Verbindungsgewichte über die Epochen.

    Args:
        activation_history (dict): Dictionary mit Aktivierungsverläufen.
        weights_history (dict): Dictionary mit Gewichtsverläufen.
    """
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    for label, activations in activation_history.items():
        if len(activations) > 0:
            plt.plot(range(1, len(activations) + 1), activations, label=label)
    plt.title("Entwicklung der Aktivierungen während des Lernens")
    plt.xlabel("Epoche")
    plt.ylabel("Aktivierung")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    for label, weights in weights_history.items():
        if len(weights) > 0:
            plt.plot(range(1, len(weights) + 1), weights, label=label, alpha=0.7)
    plt.title("Entwicklung der Verbindungsgewichte während des Lernens")
    plt.xlabel("Epoche")
    plt.ylabel("Gewicht")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# --- Visualisierung der Aktivierungs- und Gewichtsdynamik ---
def plot_dynamics(activation_history, weights_history):
    """
    Visualisiert:
    1. Entwicklung der Aktivierungen über die Zeit.
    2. Entwicklung der Verbindungsgewichte.
    3. Durchschnittlicher Gewichtsanstieg.
    4. Stabilität der Aktivierungen (Standardabweichung).

    Args:
        activation_history (dict): Dictionary mit Aktivierungsverläufen.
        weights_history (dict): Dictionary mit Gewichtsverläufen.
    """
    plt.figure(figsize=(16, 12))

    plt.subplot(2, 2, 1)
    for label, activations in activation_history.items():
        if len(activations) > 0:
            plt.plot(range(1, len(activations) + 1), activations, label=label)
    plt.title("Entwicklung der Aktivierungen während des Lernens")
    plt.xlabel("Epoche")
    plt.ylabel("Aktivierung")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    for label, weights in weights_history.items():
        if len(weights) > 0:
            plt.plot(range(1, len(weights) + 1), weights, label=label, alpha=0.7)
    plt.title("Entwicklung der Verbindungsgewichte während des Lernens")
    plt.xlabel("Epoche")
    plt.ylabel("Gewicht")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

    avg_weights = [np.mean([weights[epoch] for weights in weights_history.values() if len(weights) > epoch]) for epoch in range(len(next(iter(weights_history.values()))))]
    plt.subplot(2, 2, 3)
    plt.plot(range(1, len(avg_weights) + 1), avg_weights, label="Durchschnittliche Gewichte")
    plt.title("Durchschnittliche Entwicklung der Verbindungsgewichte")
    plt.xlabel("Epoche")
    plt.ylabel("Durchschnittliches Gewicht")
    plt.grid(True)

    std_activations = [np.std([activations[epoch] for activations in activation_history.values() if len(activations) > epoch]) for epoch in range(len(next(iter(activation_history.values()))))]
    plt.subplot(2, 2, 4)
    plt.plot(range(1, len(std_activations) + 1), std_activations, label="Stabilität (Standardabweichung)")
    plt.title("Stabilität der Aktivierungen über die Epochen")
    plt.xlabel("Epoche")
    plt.ylabel("Standardabweichung")
    plt.grid(True)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)
    plt.show()

# --- Visualisierung der Gedächtnisverteilung ---
def plot_memory_distribution(short_term_memory, mid_term_memory, long_term_memory):
    """
    Visualisiert die Verteilung der Gedächtnisknoten auf die Stufen.

    Args:
        short_term_memory (list): Liste von kurzfristigen Gedächtnisknoten.
        mid_term_memory (list): Liste von mittelfristigen Gedächtnisknoten.
        long_term_memory (list): Liste von langfristigen Gedächtnisknoten.
    """
    counts = [len(short_term_memory), len(mid_term_memory), len(long_term_memory)]
    labels = ["Kurzfristig", "Mittelfristig", "Langfristig"]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color=["red", "blue", "green"])
    plt.title("Verteilung der Gedächtnisknoten")
    plt.ylabel("Anzahl der Knoten")
    plt.show()

# --- Visualisierung der Aktivierungswerte als Heatmap ---
def plot_activation_heatmap(activation_history):
    """
    Visualisiert die Aktivierungswerte als Heatmap.

    Args:
        activation_history (dict): Dictionary mit Aktivierungsverläufen.
    """
    plt.figure(figsize=(12, 8))
    heatmap_data = np.array([activations for activations in activation_history.values() if len(activations) > 0]).T
    sns.heatmap(heatmap_data, cmap="YlGnBu", xticklabels=activation_history.keys(), yticklabels=False)
    plt.title("Heatmap der Aktivierungswerte")
    plt.xlabel("Kategorie")
    plt.ylabel("Epoche")
    plt.show()

def plot_new_brains_activation_distribution(new_brains_activation_history):
    """
    Visualisiert die Aktivierungsverteilung der neuen Gehirnmodule.

    Args:
        new_brains_activation_history (dict): Dictionary mit Aktivierungsverläufen der neuen Gehirnmodule.
    """
    plt.figure(figsize=(12, 8))
    for label, activations in new_brains_activation_history.items():
        if len(activations) > 0:
            plt.plot(range(1, len(activations) + 1), activations, label=label)

    plt.title("Aktivierungsverteilung der neuen Gehirnmodule")
    plt.xlabel("Epoche")
    plt.ylabel("Aktivierung")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_new_brains_activation_comparison(new_brains_activation_history):
    """
    Vergleicht die Aktivierungen der neuen Gehirnmodule in einem einzigen Diagramm.

    Args:
        new_brains_activation_history (dict): Dictionary mit Aktivierungsverläufen der neuen Gehirnmodule.
    """
    plt.figure(figsize=(12, 8))
    for label, activations in new_brains_activation_history.items():
        if len(activations) > 0:
            plt.plot(range(1, len(activations) + 1), activations, label=label)

    plt.title("Vergleich der Aktivierungen der neuen Gehirnmodule")
    plt.xlabel("Epoche")
    plt.ylabel("Aktivierung")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_new_brains_activation_heatmap(new_brains_activation_history):
    """
    Erstellt eine Heatmap der Aktivierungen der neuen Gehirnmodule.

    Args:
        new_brains_activation_history (dict): Dictionary mit Aktivierungsverläufen der neuen Gehirnmodule.
    """
    plt.figure(figsize=(12, 8))
    heatmap_data = np.array([activations for activations in new_brains_activation_history.values() if len(activations) > 0]).T
    sns.heatmap(heatmap_data, cmap="YlGnBu", xticklabels=new_brains_activation_history.keys(), yticklabels=False)
    plt.title("Heatmap der Aktivierungen der neuen Gehirnmodule")
    plt.xlabel("Gehirnmodul")
    plt.ylabel("Epoche")
    plt.show()

def plot_new_brains_activation_boxplot(new_brains_activation_history):
    """
    Erstellt einen Boxplot der Aktivierungen der neuen Gehirnmodule.

    Args:
        new_brains_activation_history (dict): Dictionary mit Aktivierungsverläufen der neuen Gehirnmodule.
    """
    plt.figure(figsize=(12, 8))
    data = [activations for activations in new_brains_activation_history.values() if len(activations) > 0]
    labels = list(new_brains_activation_history.keys())
    plt.boxplot(data, labels=labels)
    plt.title("Boxplot der Aktivierungen der neuen Gehirnmodule")
    plt.xlabel("Gehirnmodul")
    plt.ylabel("Aktivierung")
    plt.show()

# --- Visualisierung der Netzwerktopologie ---
def plot_network_topology(category_nodes, new_brains):
    """
    Visualisiert die Netzwerktopologie dynamisch.

    Diese Funktion visualisiert die Netzwerktopologie dynamisch mithilfe von NetworkX.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        new_brains (list): Liste der neuen Gehirnmodule.
    """
    G = nx.DiGraph()

    # Füge die bestehenden Knoten hinzu
    for node in category_nodes:
        G.add_node(node.label)
        for conn in node.connections:
            G.add_edge(node.label, conn.target_node.label, weight=conn.weight)

    # Füge die neuen Gehirnmodule hinzu
    for brain in new_brains:
        G.add_node(brain.label, color='red')
        for conn in brain.connections:
            G.add_edge(brain.label, conn.target_node.label, weight=conn.weight)

    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    node_colors = [G.nodes[node].get('color', 'skyblue') for node in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight="bold", edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Netzwerktopologie")
    plt.show()

def save_model(category_nodes, filename="model.json"):
    """
    Speichert die Gewichte der Verbindungen und andere relevante Informationen in einer Datei.

    Diese Funktion speichert die Gewichte der Verbindungen und andere relevante Informationen in einer JSON-Datei.

    Args:
        category_nodes (list): Liste von Knotenobjekten.
        filename (str): Name der Datei.
    """
    model_data = {
        "nodes": [],
        "connections": []
    }

    for node in category_nodes:
        model_data["nodes"].append({
            "label": node.label,
            "activation": node.activation,
            "activation_history": node.activation_history if hasattr(node, "activation_history") else []
        })
        for conn in node.connections:
            model_data["connections"].append({
                "source": node.label,
                "target": conn.target_node.label,
                "weight": conn.weight
            })

    with open(filename, "w") as file:
        json.dump(model_data, file, indent=4)

    print(f"Modell gespeichert in {filename}")

def load_model(filename="model.json"):
    """
    Lädt die Gewichte der Verbindungen und andere relevante Informationen aus einer Datei.

    Diese Funktion lädt die Gewichte der Verbindungen und andere relevante Informationen aus einer JSON-Datei.

    Args:
        filename (str): Name der Datei.

    Returns:
        list: Liste von Knotenobjekten.
    """
    if not os.path.exists(filename):
        print(f"Datei {filename} nicht gefunden. Netzwerk wird initialisiert.")
        return None

    with open(filename, "r") as file:
        model_data = json.load(file)

    category_nodes = []
    node_dict = {}

    for node_data in model_data["nodes"]:
        node = Node(node_data["label"])
        node.activation = node_data["activation"]
        if "activation_history" in node_data:
            node.activation_history = node_data["activation_history"]
        category_nodes.append(node)
        node_dict[node_data["label"]] = node

    for conn_data in model_data["connections"]:
        source_node = node_dict[conn_data["source"]]
        target_node = node_dict[conn_data["target"]]
        connection = Connection(target_node, conn_data["weight"])
        source_node.connections.append(connection)

    return category_nodes

# --- Erweiterte Visualisierungen ---
def create_dashboard(activation_history, short_term_memory, mid_term_memory, long_term_memory):
    # Streamlit Dashboard
    st.title("Gedächtnisprozesse und Aktivierungsverläufe")

    # Verteilung der Gedächtnisknoten
    st.header("Verteilung der Gedächtnisknoten")
    memory_data = {
        "Typ": ["Kurzfristig", "Mittelfristig", "Langfristig"],
        "Anzahl": [len(short_term_memory), len(mid_term_memory), len(long_term_memory)]
    }
    memory_fig = px.bar(memory_data, x="Typ", y="Anzahl", title="Gedächtnisverteilung")
    st.plotly_chart(memory_fig)

    # Aktivierungsverläufe
    st.header("Aktivierungsverläufe")
    for label, activations in activation_history.items():
        st.line_chart(activations)

def plot_3d_network(category_nodes):
    G = nx.DiGraph()
    for node in category_nodes:
        G.add_node(node.label)
        for conn in node.connections:
            G.add_edge(node.label, conn.target_node.label, weight=conn.weight)

    pos = nx.spring_layout(G, dim=3)
    x_nodes = [pos[k][0] for k in G.nodes()]
    y_nodes = [pos[k][1] for k in G.nodes()]
    z_nodes = [pos[k][2] for k in G.nodes()]

    edge_trace = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_trace.append(go.Scatter3d(x=[x0, x1], y=[y0, y1], z=[z0, z1],
                                        mode='lines', line=dict(color='blue', width=1)))

    node_trace = go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes,
                                mode='markers', marker=dict(size=10, color='red'))

    layout = go.Layout(title="3D Netzwerktopologie", showlegend=False)
    fig = go.Figure(data=edge_trace + [node_trace], layout=layout)

    # Speichern statt Blockieren
    fig.write_html("network_topology.html")
    print("Das 3D-Diagramm wurde unter 'network_topology.html' gespeichert. Öffnen Sie diese Datei in einem Browser.")

    
def run_3d_plot(category_nodes):
    plot_3d_network(category_nodes)
    

def gpu_accelerated_propagation(input_signal, weights):
    input_tensor = torch.tensor(input_signal, device='cuda')
    weight_tensor = torch.tensor(weights, device='cuda')
    output = torch.matmul(input_tensor, weight_tensor)
    return output.cpu().numpy()

def compute(input_signal, weights, use_gpu=False):
    if use_gpu:
        return gpu_accelerated_propagation(input_signal, weights)
    else:
        return np.dot(input_signal, weights)



def plot_new_ideas(new_ideas_history):
    """
    Visualisiert die Anzahl der neuen Ideen pro Epoche.

    Args:
        new_ideas_history (list): Liste der neuen Ideen pro Epoche.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(new_ideas_history) + 1), new_ideas_history, marker='o')
    plt.title("Anzahl der neuen Ideen pro Epoche")
    plt.xlabel("Epoche")
    plt.ylabel("Anzahl der neuen Ideen")
    plt.grid(True)
    plt.show()

def plot_scenarios(scenarios_history):
    """
    Visualisiert die Anzahl der simulierten Szenarien pro Epoche.

    Args:
        scenarios_history (list): Liste der simulierten Szenarien pro Epoche.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(scenarios_history) + 1), scenarios_history, marker='o')
    plt.title("Anzahl der simulierten Szenarien pro Epoche")
    plt.xlabel("Epoche")
    plt.ylabel("Anzahl der Szenarien")
    plt.grid(True)
    plt.show()

def plot_evaluated_ideas(evaluated_ideas_history):
    """
    Visualisiert die Bewertungen der Ideen.

    Args:
        evaluated_ideas_history (list): Liste der bewerteten Ideen.
    """
    scores = [float(idea.split("Score: ")[1]) for idea in evaluated_ideas_history]
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=10, edgecolor='black')
    plt.title("Bewertungen der Ideen")
    plt.xlabel("Bewertung")
    plt.ylabel("Anzahl der Ideen")
    plt.grid(True)
    plt.show()

def plot_emotional_weights(weighted_ideas_history):
    """
    Visualisiert die emotionalen Gewichtungen der Ideen.

    Args:
        weighted_ideas_history (list): Liste der emotional gewichteten Ideen.
    """
    weights = [float(idea.split("Weight: ")[1]) for idea in weighted_ideas_history]
    plt.figure(figsize=(10, 6))
    plt.hist(weights, bins=10, edgecolor='black')
    plt.title("Emotionale Gewichtungen der Ideen")
    plt.xlabel("Gewichtung")
    plt.ylabel("Anzahl der Ideen")
    plt.grid(True)
    plt.show()

def plot_social_interactions(interactions_history):
    """
    Visualisiert die Anzahl der sozialen Interaktionen pro Epoche.

    Args:
        interactions_history (list): Liste der sozialen Interaktionen pro Epoche.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(interactions_history) + 1), interactions_history, marker='o')
    plt.title("Anzahl der sozialen Interaktionen pro Epoche")
    plt.xlabel("Epoche")
    plt.ylabel("Anzahl der Interaktionen")
    plt.grid(True)
    plt.show()


def main():
    """
    Hauptfunktion, die die Simulation ausführt und die Ergebnisse visualisiert.

    Diese Funktion führt die Simulation aus und visualisiert die Ergebnisse.
    """
    start_time = time.time()

    csv_file = "data.csv"
    data = pd.read_csv(csv_file)
    categories = data['Kategorie'].unique()

    category_nodes = load_model("model.json")
    if category_nodes is None:
        category_nodes = initialize_quiz_network(categories)

    personality_distributions = {category: random.uniform(0.5, 0.8) for category in categories}

    activation_history, weights_history = simulate_learning(
        data, category_nodes, personality_distributions, epochs=100, learning_rate=0.8, reward_interval=5, decay_rate=0.002
    )

    save_model(category_nodes, "model.json")

    # Erstellen Sie Instanzen der neuen Gehirnmodule
    cortex_creativus = CortexCreativus("Cortex Creativus")
    simulatrix_neuralis = SimulatrixNeuralis("Simulatrix Neuralis")
    cortex_criticus = CortexCriticus("Cortex Criticus")
    limbus_affektus = LimbusAffektus("Limbus Affektus")
    meta_cognitio = MetaCognitio("Meta Cognitio")
    cortex_socialis = CortexSocialis("Cortex Socialis")

    # Verbinden Sie die neuen Gehirnmodule mit den bestehenden Knoten
    connect_new_brains_to_network(category_nodes, [cortex_creativus, simulatrix_neuralis, cortex_criticus, limbus_affektus, meta_cognitio, cortex_socialis])

    # Speichern der Ergebnisse der neuen Gehirnmodule
    new_ideas_history = []
    scenarios_history = []
    evaluated_ideas_history = []
    weighted_ideas_history = []
    interactions_history = []

    for epoch in range(100):
        new_ideas = cortex_creativus.generate_new_ideas(category_nodes)
        scenarios = simulatrix_neuralis.simulate_scenarios(category_nodes)
        evaluated_ideas = cortex_criticus.evaluate_ideas(new_ideas)
        emotional_state = 0.7  # Beispielwert für emotionalen Zustand
        weighted_ideas = limbus_affektus.apply_emotional_weight(evaluated_ideas, emotional_state)
        meta_cognitio.optimize_system(category_nodes)
        interactions = cortex_socialis.simulate_social_interactions(category_nodes)

        new_ideas_history.append(len(new_ideas))
        scenarios_history.append(len(scenarios))
        evaluated_ideas_history.extend(evaluated_ideas)
        weighted_ideas_history.extend(weighted_ideas)
        interactions_history.append(len(interactions))

    # Visualisieren Sie die Ergebnisse der neuen Gehirnmodule
    plot_new_ideas(new_ideas_history)
    plot_scenarios(scenarios_history)
    plot_evaluated_ideas(evaluated_ideas_history)
    plot_emotional_weights(weighted_ideas_history)
    plot_social_interactions(interactions_history)

    # Speichern der Aktivierungsverläufe der neuen Gehirnmodule
    new_brains_activation_history = {brain.label: [] for brain in [cortex_creativus, simulatrix_neuralis, cortex_criticus, limbus_affektus, meta_cognitio, cortex_socialis]}
    for epoch in range(100):
        for brain in [cortex_creativus, simulatrix_neuralis, cortex_criticus, limbus_affektus, meta_cognitio, cortex_socialis]:
            input_signal = random.uniform(0.1, 1.0)
            propagate_signal(brain, input_signal, {}, 1.0, {})
            new_brains_activation_history[brain.label].append(brain.activation)

    plot_dynamics(activation_history, weights_history)
    plot_activation_heatmap(activation_history)
    plot_network_topology(category_nodes, [cortex_creativus, simulatrix_neuralis, cortex_criticus, limbus_affektus, meta_cognitio, cortex_socialis])
    plot_new_brains_activation_distribution(new_brains_activation_history)
    plot_new_brains_activation_comparison(new_brains_activation_history)
    plot_new_brains_activation_heatmap(new_brains_activation_history)
    plot_new_brains_activation_boxplot(new_brains_activation_history)

    short_term_memory, mid_term_memory, long_term_memory = simulate_multilevel_memory(data, category_nodes, personality_distributions, epochs=100)

    plot_memory_distribution(short_term_memory, mid_term_memory, long_term_memory)

    # Erweiterte Visualisierungen
    create_dashboard(activation_history, short_term_memory, mid_term_memory, long_term_memory)

    # Starten Sie die 3D-Visualisierung in einem separaten Thread
    t = threading.Thread(target=run_3d_plot, args=(category_nodes,))
    t.start()

    end_time = time.time()
    print(f"Gesamtausführungszeit: {end_time - start_time:.4f} Sekunden")




def run_simulation_from_gui(learning_rate, decay_rate, reward_interval, epochs):
    """
    Führt die Simulation mit den GUI-Einstellungen aus und visualisiert die Ergebnisse.

    Diese Funktion führt die Simulation mit den GUI-Einstellungen aus und visualisiert die Ergebnisse.

    Args:
        learning_rate (float): Lernrate.
        decay_rate (float): Rate, mit der die Gewichte abnehmen.
        reward_interval (int): Intervall für Belohnungen.
        epochs (int): Anzahl der Epochen.
    """
    start_time = time.time()

    csv_file = "data.csv"
    data = pd.read_csv(csv_file)
    categories = data['Kategorie'].unique()

    category_nodes = load_model("model.json")
    if category_nodes is None:
        category_nodes = initialize_quiz_network(categories)

    personality_distributions = {category: random.uniform(0.5, 0.8) for category in categories}

    activation_history, weights_history = simulate_learning(
        data, category_nodes, personality_distributions,
        epochs=int(epochs),
        learning_rate=float(learning_rate),
        reward_interval=int(reward_interval),
        decay_rate=float(decay_rate)
    )

    save_model(category_nodes, "model.json")

    new_brains = [CortexCreativus("Cortex Creativus"), SimulatrixNeuralis("Simulatrix Neuralis"), CortexCriticus("Cortex Criticus"), LimbusAffektus("Limbus Affektus"), MetaCognitio("Meta Cognitio"), CortexSocialis("Cortex Socialis")]
    connect_new_brains_to_network(category_nodes, new_brains)

    # Speichern der Aktivierungsverläufe der neuen Gehirnmodule
    new_brains_activation_history = {brain.label: [] for brain in new_brains}
    for epoch in range(int(epochs)):
        for brain in new_brains:
            input_signal = random.uniform(0.1, 1.0)
            propagate_signal(brain, input_signal, {}, 1.0, {})
            new_brains_activation_history[brain.label].append(brain.activation)

    plot_dynamics(activation_history, weights_history)
    plot_activation_heatmap(activation_history)
    plot_network_topology(category_nodes, new_brains)
    plot_new_brains_activation_distribution(new_brains_activation_history)
    plot_new_brains_activation_comparison(new_brains_activation_history)
    plot_new_brains_activation_heatmap(new_brains_activation_history)
    plot_new_brains_activation_boxplot(new_brains_activation_history)


    short_term_memory, mid_term_memory, long_term_memory = simulate_multilevel_memory(data, category_nodes, personality_distributions, epochs=int(epochs))

    plot_memory_distribution(short_term_memory, mid_term_memory, long_term_memory)

    # Erweiterte Visualisierungen
    create_dashboard(activation_history, short_term_memory, mid_term_memory, long_term_memory)
    plot_3d_network(category_nodes)

    end_time = time.time()
    print(f"Gesamtausführungszeit: {end_time - start_time:.4f} Sekunden")

def start_gui():
    """
    Erstellt eine grafische Benutzeroberfläche, um Parameter für die Simulation anzupassen und zu starten.

    Diese Funktion erstellt eine grafische Benutzeroberfläche, um Parameter für die Simulation anzupassen und zu starten.
    """

    def start_simulation():
        learning_rate = float(learning_rate_entry.get())
        decay_rate = float(decay_rate_entry.get())
        reward_interval = int(reward_interval_entry.get())
        epochs = int(epochs_entry.get())
        run_simulation_from_gui(learning_rate, decay_rate, reward_interval, epochs)

    root = tk.Tk()
    root.title("Psyco Simulation GUI")
    root.geometry("400x300")

    header_label = tk.Label(root, text="Simulationseinstellungen", font=("Helvetica", 16))
    header_label.pack(pady=10)

    learning_rate_label = tk.Label(root, text="Lernrate:")
    learning_rate_label.pack()
    learning_rate_entry = tk.Entry(root)
    learning_rate_entry.insert(0, "0.8")
    learning_rate_entry.pack()

    decay_rate_label = tk.Label(root, text="Vergessensrate:")
    decay_rate_label.pack()
    decay_rate_entry = tk.Entry(root)
    decay_rate_entry.insert(0, "0.002")
    decay_rate_entry.pack()

    reward_interval_label = tk.Label(root, text="Belohnungsintervall:")
    reward_interval_label.pack()
    reward_interval_entry = tk.Entry(root)
    reward_interval_entry.insert(0, "5")
    reward_interval_entry.pack()

    epochs_label = tk.Label(root, text="Anzahl der Epochen:")
    epochs_label.pack()
    epochs_entry = tk.Entry(root)
    epochs_entry.insert(0, "5")
    epochs_entry.pack()

    start_button = tk.Button(root, text="Simulation starten", command=start_simulation)
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
