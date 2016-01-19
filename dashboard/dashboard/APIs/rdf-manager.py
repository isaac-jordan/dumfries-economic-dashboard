import rdflib

def start():
    dumfriesDataZone = "Data Zone S01001053"
    dumfriesDataZoneID = "S01001053"
    g = rdflib.Graph()
    result = g.parse("http://data.opendatascotland.org/data/simd/income-rank/2012/S01001053.nt", format="nt")
    
    print("graph has %s statements." % len(g))
    import pprint
    
    for stmt in g:
        pprint.pprint(g)
    print(g.serialize(format="n3"))
    
if __name__ == "__main__":
    start()
    