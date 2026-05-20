'use client'
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

const MOCK_SITES = [
  {id:'CO-BOG-001',lat:4.65,lon:-74.08,city:'Bogota',edge:15,type:'macro'},
  {id:'CO-BOG-002',lat:4.68,lon:-74.05,city:'Bogota',edge:12,type:'macro'},
  {id:'CO-BOG-003',lat:4.60,lon:-74.10,city:'Bogota',edge:22,type:'macro'},
  {id:'CO-MED-001',lat:6.25,lon:-75.57,city:'Medellin',edge:18,type:'macro'},
  {id:'CO-MED-002',lat:6.22,lon:-75.55,city:'Medellin',edge:16,type:'macro'},
  {id:'CO-CAL-001',lat:3.43,lon:-76.52,city:'Cali',edge:24,type:'macro'},
  {id:'CO-CAL-002',lat:3.40,lon:-76.50,city:'Cali',edge:20,type:'macro'},
  {id:'CO-BAR-001',lat:10.98,lon:-74.79,city:'Barranquilla',edge:35,type:'macro'},
  {id:'CO-BAR-002',lat:10.96,lon:-74.78,city:'Barranquilla',edge:32,type:'macro'},
  {id:'CO-BAR-003',lat:11.00,lon:-74.80,city:'Barranquilla',edge:38,type:'macro'},
  {id:'CO-CAR-001',lat:10.41,lon:-75.52,city:'Cartagena',edge:28,type:'macro'},
  {id:'CO-CAR-002',lat:10.39,lon:-75.50,city:'Cartagena',edge:30,type:'macro'},
]

function getColor(edge: number) {
  if (edge < 20) return '#10b981'
  if (edge < 30) return '#f59e0b'
  return '#ef4444'
}

export default function MapInner() {
  return (
    <MapContainer center={[5.5, -74.5]} zoom={6} style={{height:'100%',width:'100%',borderRadius:'0.5rem'}} zoomControl={false}>
      <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='&copy; CartoDB' />
      {MOCK_SITES.map(s => (
        <CircleMarker key={s.id} center={[s.lat,s.lon]} radius={7} pathOptions={{color:getColor(s.edge),fillColor:getColor(s.edge),fillOpacity:0.8,weight:1}}>
          <Popup>
            <div className="text-xs">
              <p className="font-bold">{s.id}</p>
              <p>{s.city}</p>
              <p>边缘占比: {s.edge}%</p>
              <a href={`/drilldown/${s.city}`} className="text-blue-500 underline">下钻 →</a>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  )
}
