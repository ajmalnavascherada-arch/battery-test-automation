import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# File Path (YOUR PATH)
# -----------------------------
FILE_PATH = r"C:\Users\Ajmal\battery_automation\sample_battery_data.csv"

# -----------------------------
# Load Data
# -----------------------------
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("✅ Data loaded successfully.\n")
        print(df.head())
        return df
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        exit()

# -----------------------------
# Capacity Analysis
# -----------------------------
def calculate_capacity(df):
    capacity = df.groupby('Cycle')['Capacity'].max()
    print("\n📊 Capacity per cycle:\n", capacity)
    return capacity

# -----------------------------
# Efficiency Calculation
# -----------------------------
def calculate_efficiency(df):
    efficiency = []

    for cycle in df['Cycle'].unique():
        cycle_data = df[df['Cycle'] == cycle]

        charge = cycle_data[cycle_data['Current'] > 0]['Capacity'].max()
        discharge = cycle_data[cycle_data['Current'] < 0]['Capacity'].min()

        if charge != 0:
            eff = abs(discharge) / charge * 100
        else:
            eff = 0

        efficiency.append((cycle, eff))

    eff_df = pd.DataFrame(efficiency, columns=['Cycle', 'Efficiency'])
    print("\n⚡ Efficiency:\n", eff_df)
    return eff_df

def plot_capacity(capacity):
    plt.figure()
    capacity.plot(marker='o')
    plt.xlabel("Cycle")
    plt.ylabel("Capacity (Ah)")
    plt.title("Capacity Fade")
    plt.grid()
    plt.savefig("capacity_fade.png")
    plt.show()  # 👈 IMPORTANT
    print("📉 capacity_fade.png saved")
def plot_voltage(df):
    plt.figure()

    for cycle in df['Cycle'].unique():
        cycle_data = df[df['Cycle'] == cycle]
        plt.plot(cycle_data['Time'], cycle_data['Voltage'], label=f'Cycle {cycle}')

    plt.xlabel("Time")
    plt.ylabel("Voltage (V)")
    plt.title("Voltage vs Time")
    plt.legend()
    plt.grid()
    plt.savefig("voltage_plot.png")
    plt.show()  # 👈 IMPORTANT
    print("📈 voltage_plot.png saved")

# -----------------------------
# Generate Report
# -----------------------------
def generate_report(capacity, efficiency):
    with open("report.txt", "w") as f:
        f.write("Battery Analysis Report\n")
        f.write("========================\n\n")

        f.write("Capacity per Cycle:\n")
        f.write(capacity.to_string())
        f.write("\n\n")

        f.write("Efficiency (%):\n")
        f.write(efficiency.to_string(index=False))
        f.write("\n\n")

        initial = capacity.iloc[0]
        final = capacity.iloc[-1]
        fade = ((initial - final) / initial) * 100

        f.write("Summary:\n")
        f.write(f"Initial Capacity: {initial:.3f} Ah\n")
        f.write(f"Final Capacity: {final:.3f} Ah\n")
        f.write(f"Capacity Fade: {fade:.2f} %\n")

    print("📄 report.txt saved")

# -----------------------------
# Main
# -----------------------------
def main():
    if not os.path.exists(FILE_PATH):
        print("❌ File not found. Check your path.")
        return

    print(f"📂 Using file:\n{FILE_PATH}\n")

    df = load_data(FILE_PATH)

    capacity = calculate_capacity(df)
    efficiency = calculate_efficiency(df)

    plot_capacity(capacity)
    plot_voltage(df)
    generate_report(capacity, efficiency)

    print("\n✅ DONE — All outputs generated.")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main()