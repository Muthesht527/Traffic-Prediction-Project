import { Link } from 'react-router-dom';
import { MapPin, Cloud, Brain, ArrowRight } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50">
      {/* Header */}
      <header className="px-6 py-5">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
              <MapPin className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">Traffic Forecast</span>
          </div>
          <Link
            to="/forecast"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-xl font-semibold hover:bg-secondary transition-colors"
          >
            Get Started
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      {/* Hero */}
      <main className="max-w-6xl mx-auto px-6 pt-12 pb-24">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight">
            AI-Powered <span className="text-primary">Traffic Forecast</span> Visualization
          </h1>
          <p className="mt-6 text-xl text-gray-600 leading-relaxed">
            Predict future traffic congestion and visualize it on an interactive map.
            Select your route, pick a date and time — our machine learning engine forecasts
            congestion so you can plan ahead.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/forecast"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-primary text-white rounded-2xl font-bold text-lg hover:bg-secondary transition-colors shadow-lg shadow-primary/25"
            >
              <MapPin className="w-5 h-5" />
              Open Forecast Map
            </Link>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="mt-20 grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Cloud className="w-7 h-7 text-primary" />}
            title="Weather-Aware"
            description="Automatically fetches weather forecasts — temperature, humidity, rain, and wind become prediction inputs."
          />
          <FeatureCard
            icon={<Brain className="w-7 h-7 text-primary" />}
            title="ML Predictions"
            description="A Random Forest model analyses historical traffic patterns to predict congestion scores from 0–100."
          />
          <FeatureCard
            icon={<MapPin className="w-7 h-7 text-primary" />}
            title="Map Visualization"
            description="Routes are colour-coded like Google Maps traffic — green for free-flow, red for heavy congestion."
          />
        </div>

        {/* How It Works */}
        <div className="mt-24">
          <h2 className="text-3xl font-bold text-center text-gray-900">How It Works</h2>
          <div className="mt-12 grid md:grid-cols-4 gap-6">
            <StepCard step="1" title="Select Route" text="Choose source and destination on the map" />
            <StepCard step="2" title="Pick Time" text="Set a future date and time for the forecast" />
            <StepCard step="3" title="AI Predicts" text="Backend fetches weather & runs the ML model" />
            <StepCard step="4" title="See Results" text="View colour-coded congestion on the map" />
          </div>
        </div>

        {/* Coverage Notice */}
        <div className="mt-20 p-6 bg-amber-50 border border-amber-200 rounded-2xl text-center">
          <p className="text-amber-800 font-medium">
            📍 Currently supporting <strong>Chennai, India</strong>. Roads outside the dataset coverage area are shown in grey.
          </p>
        </div>
      </main>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="p-6 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
      <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-bold text-gray-900">{title}</h3>
      <p className="mt-2 text-gray-600 text-sm leading-relaxed">{description}</p>
    </div>
  );
}

function StepCard({ step, title, text }) {
  return (
    <div className="text-center p-5">
      <div className="w-12 h-12 rounded-full bg-primary text-white font-bold text-xl flex items-center justify-center mx-auto mb-3">
        {step}
      </div>
      <h4 className="font-bold text-gray-900">{title}</h4>
      <p className="text-sm text-gray-600 mt-1">{text}</p>
    </div>
  );
}
