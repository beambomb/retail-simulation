class SimulationService {
    static async fetchMetrics() {
        const response = await fetch('/api/metrics');
        if (!response.ok) {
            throw new Error('Failed to load metrics');
        }
        return await response.json();
    }

    static async triggerSimulation(params) {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params),
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.message || 'Simulation execution failed');
        }
        return await response.json();
    }
}
