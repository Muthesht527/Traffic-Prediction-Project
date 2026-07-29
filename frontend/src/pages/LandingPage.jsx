import { Link } from 'react-router-dom';
import {
  MapPin,
  Cloud,
  Brain,
  ArrowRight,
  Calendar,
  Navigation,
  BarChart3,
  Globe,
  Shield,
  Zap,
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50 overflow-hidden">
      {/* Header */}
      <header className="px-6 py-5">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center shadow-lg shadow-orange-500/20">
              <MapPin className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">Traffic Forecast</span>
          </div>
          <Link
            to="/forecast"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl font-semibold hover:from-orange-600 hover:to-red-600 transition-all shadow-lg shadow-orange-500/20 hover:shadow-orange-500/30 active:scale-95"
          >
            Open Forecast
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      {/* Hero */}
      <main className="max-w-6xl mx-auto px-6 pt-8 pb-20">
        <div className="text-center max-w-3xl mx-auto animate-slide-up">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white rounded-full border border-orange-100 text-orange-700 text-xs font-medium mb-6 shadow-sm">
            <Zap className="w-3.5 h-3.5" />
            AI-Powered Traffic Intelligence
          </div>
          <h1 className="text-5xl md:text-6xl font-black text-gray-900 leading-tight">
            Forecast Traffic,{' '}
            <span className="bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
              Not Just Track It
            </span>
          </h1>
          <p className="mt-6 text-lg text-gray-600 leading-relaxed max-w-2xl mx-auto">
            Predict future traffic congestion up to 7 days ahead and visualize it on an interactive map.
            Powered by machine learning, weather forecasts, and historical traffic patterns.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/forecast"
              className="group inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-2xl font-bold text-lg hover:from-orange-600 hover:to-red-600 transition-all shadow-xl shadow-orange-500/25 hover:shadow-orange-500/35 active:scale-95"
            >
              <MapPin className="w-5 h-5" />
              Start Forecasting
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="mt-20 grid md:grid-cols-3 gap-6">
          <FeatureCard
            icon={<Cloud className="w-7 h-7" />}
            title="Weather-Aware Predictions"
            description="Automatically fetches weather forecasts — temperature, humidity, rain, and wind become ML inputs."
            gradient="from-blue-500 to-cyan-500"
            delay={0}
          />
          <FeatureCard
            icon={<Brain className="w-7 h-7" />}
            title="Random Forest ML"
            description="300-tree ensemble model trained on 5,000+ samples. R² = 0.94, MAE = 4.0. Explainable and fast."
            gradient="from-purple-500 to-pink-500"
            delay={1}
          />
          <FeatureCard
            icon={<Navigation className="w-7 h-7" />}
            title="Google Maps-Style Routes"
            description="Routes are colour-coded: green for free-flow, red for heavy congestion. Interactive Leaflet map."
            gradient="from-orange-500 to-red-500"
            delay={2}
          />
        </div>

        {/* How It Works */}
        <div className="mt-24">
          <h2 className="text-3xl font-black text-center text-gray-900">How It Works</h2>
          <p className="text-center text-gray-500 mt-2 max-w-xl mx-auto">
            Four simple steps from input to visualization
          </p>
          <div className="mt-12 grid md:grid-cols-4 gap-6">
            <StepCard
              icon={<MapPin className="w-6 h-6" />}
              step="1"
              title="Select Route"
              text="Type source and destination with autocomplete"
              gradient="from-green-500 to-emerald-500"
            />
            <StepCard
              icon={<Calendar className="w-6 h-6" />}
              step="2"
              title="Pick Time"
              text="Choose any date and time up to 7 days ahead"
              gradient="from-blue-500 to-cyan-500"
            />
            <StepCard
              icon={<Brain className="w-6 h-6" />}
              step="3"
              title="AI Predicts"
              text="Backend fetches weather, routes, and runs ML"
              gradient="from-purple-500 to-pink-500"
            />
            <StepCard
              icon={<BarChart3 className="w-6 h-6" />}
              step="4"
              title="See Results"
              text="View colour-coded congestion on the map"
              gradient="from-orange-500 to-red-500"
            />
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-24 p-8 bg-white rounded-3xl border border-gray-100 shadow-sm">
          <h2 className="text-2xl font-black text-center text-gray-900 mb-8">Built With</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <TechBadge label="React + Vite" icon="⚛️" />
            <TechBadge label="Flask API" icon="🐍" />
            <TechBadge label="Scikit-Learn" icon="🧠" />
            <TechBadge label="Leaflet + OSM" icon="🗺️" />
            <TechBadge label="TailwindCSS" icon="🎨" />
            <TechBadge label="Random Forest" icon="🌲" />
            <TechBadge label="OpenWeather" icon="☁️" />
            <TechBadge label="Nominatim" icon="📍" />
          </div>
        </div>

        {/* Coverage Notice */}
        <div className="mt-12 p-6 bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-100 rounded-2xl text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Globe className="w-5 h-5 text-amber-600" />
            <p className="text-amber-800 font-bold text-sm">
              Phase 1 Coverage: Chennai, India
            </p>
          </div>
          <p className="text-amber-700/80 text-xs">
            Roads outside the dataset coverage area are shown in grey with "Coverage Not Available" — never faked.
          </p>
        </div>

        {/* Architecture */}
        <div className="mt-12 p-6 bg-gray-50 rounded-2xl border border-gray-100">
          <div className="flex items-center gap-2 mb-3">
            <Shield className="w-5 h-5 text-gray-600" />
            <h3 className="font-bold text-gray-800">Modular Architecture</h3>
          </div>
          <p className="text-sm text-gray-600 leading-relaxed">
            Designed for scalability. Future phases can integrate YOLO vehicle detection, CCTV feeds,
            IoT sensors, automatic model retraining, and city-wide expansion — without redesigning
            the core prediction engine.
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-orange-100 py-6 text-center text-sm text-gray-500">
        <p>AI-Powered Traffic Forecast Visualization Platform — Phase 1 Hackathon MVP</p>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description, gradient, delay }) {
  return (
    <div
      className="group p-6 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
      style={{ animationDelay: `${delay * 100}ms` }}
    >
      <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white mb-4 shadow-lg group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <h3 className="text-lg font-bold text-gray-900">{title}</h3>
      <p className="mt-2 text-gray-600 text-sm leading-relaxed">{description}</p>
    </div>
  );
}

function StepCard({ icon, step, title, text, gradient }) {
  return (
    <div className="text-center p-5 group">
      <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${gradient} text-white font-black text-lg flex items-center justify-center mx-auto mb-3 shadow-lg group-hover:scale-110 transition-transform`}>
        {step}
      </div>
      <div className="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center mx-auto mb-2 text-gray-600">
        {icon}
      </div>
      <h4 className="font-bold text-gray-900 text-sm">{title}</h4>
      <p className="text-xs text-gray-500 mt-1">{text}</p>
    </div>
  );
}

function TechBadge({ label, icon }) {
  return (
    <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-200 transition-colors">
      <span className="text-lg">{icon}</span>
      <span className="text-sm font-medium text-gray-700">{label}</span>
    </div>
  );
}
