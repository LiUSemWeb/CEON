# Circular Enabler Category 2 – SPARQL Queries

All queries assume the [common prefixes](index.md#prefixes) are declared.

---

## CQ-CE-5-1

**What are the barriers or missing actors/processes/resources to implement a resource exchange/material flow?**

---

## CQ-CE-5-2

**What is the material breakdown of a product or component?**

```sparql
SELECT ?physicalObject ?component
WHERE {
    ?physicalObject rdf:type resourceODP:PhysicalObject .
    ?physicalObject resource:hasMatter ?material .
    ?material material:hasMaterialComponent ?component .
}
```

---

## CQ-CE-5-3

**In what units of measure are values expressed?**

---

## CQ-CE-5-4

**What is the quality of a flow at a specific time?**

---

## CQ-CE-5-5

**What is the quantity of a flow at a specific time?**

---

## CQ-CE-5-6

**From what source does this data originate?**

---

## CQ-CE-5-7

**What are the elements (e.g. steps/work and actors) involved in this process?**

- **Same as:** [CQ-CE-3-4.sparql](../sparql/cec1.md#cq-ce-3-4)

---

## CQ-CE-5-8

**What is the origin and complete trace of this material?**

---

## CQ-CE-5-9

**What is the overall energy consumption to produce this material/component/product?**

```sparql
SELECT ?execution ?energy
WHERE {
    ?execution processODP:isSettingFor ?process.
    ?energy rdf:type process:Energy .
    ?process process:needsEnergy ?energy .
}
```

---

## CQ-CE-5-10

**What are the rebound effects and added energy requirements of a material flow?**

---

## CQ-CE-5-11

**What are the alternatives to this flow?**

---

## CQ-CE-5-12

**What are the energy demands of this process?**

```sparql
SELECT ?energy
WHERE {
    ?energy rdf:type process:Energy .
    ?process process:needsEnergy ?energy .
}
```

---

## CQ-CE-5-13

**What are the technical and/or economic requirements of implementing this process/strategy?**

- **Same as:** [CQ-CE-3-1.sparql](../sparql/cec1.md#cq-ce-3-1)

---

## CQ-CE-5-14

**What effects would it have on external social and environmental factors?**

---

## CQ-CE-5-15

**What are the needs in terms of social and environmental factors?**

```sparql
SELECT ?capability ?resourcerelation
WHERE {
    ?capability rdf:type actorODP:Capability .
    ?capability actor:neededResourceRelation ?resourcerelation . 
}
```

---

## CQ-CE-5-16

**What is the value proposition of the overall value network and life cycle?**

```sparql
SELECT ?cvn ?valueProposition
WHERE {
    ?cvn rdf:type cvn:CVN .
    ?cvn cvn:aimsAtValue ?valuePropostition .
    ?valueProposition rdf:type value:ValueProposition .
}
```

---

## CQ-CE-5-17

**What are the activities related to this value creation, capture and delivery?**

```sparql
SELECT ?process ?perception
WHERE{
    ?perception rdf:type value:ValuePerception .
    ?perception value:onValueParticipation ?participation .
    ?proposition value:targetingParticipation ?participation .
    ?cvn cvn:aimsAtValue ?proposition .
    ?cvn cvn:composedOf ?process .
}
```

---

## CQ-CE-5-18

**What are the objectives of this value network/actor/process?**

```sparql
SELECT ?cvn ?valueProposition
WHERE{
    ?cvn rdf:type cvn:CVN .
    ?cvn cvn:aimsAtValue ?valueProposition .
    ?cvn cvn:composedOf ?process .
}
```

---

## CQ-CE-5-19

**What is the value created/missed/destroyed by this flow/process?**

```sparql
SELECT ?process ?value
WHERE{
    ?process cvn:createsValue ?value .
    ?value rdf:type value:Value .
}
```

---

## CQ-CE-6-1

**What external factors affect this process/actor/value network?**

---

## CQ-CE-6-2

**What is the legal conditions and legislation affecting this actor/object/process?**

---

## CQ-CE-6-3

**What is the energy infrastructure available?**

```sparql
SELECT ?infra
WHERE{
    ?infra rdf:type energy:EnergyInfrastruture .
}
```

---

## CQ-CE-7-1

**What were the methods/algorithms used to measure or assess a certain value or decision, and what input data was used?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-7-2

**What are the direct/indirect effects/outcomes of an action?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-7-3

**Was the (material, information) exchange successful?**

---

## CQ-CE-7-4

**What is the energy consumption of an action/process?**

- **Same as:** [CQ-CE-5-12.sparql](../sparql/cec2.md#cq-ce-5-12)

---

## CQ-CE-7-5

**What is the carbon emission of an action/process?**

```sparql
SELECT ?process ?CO2
WHERE {
    ?process process:producesCO2 ?CO2 .
}
```

---

## CQ-CE-7-6

**At what time did this energy data change, and what is its detailed breakdown?**

```sparql
SELECT ?energyComposition ?percentage
WHERE {
    ?energyComposition actorODP:participatingObject energy:Energy .
    ?energyComposition energy:hasEnergyComponentPercentage ?percentage .
}
```

---

## CQ-CE-7-7

**What are the potential rebound effects of this action/process?**

---

## CQ-CE-7-8

**What is the economic, environmental and social value created/missed/destroyed by a process?**

- **Same as:** [CQ-CE-5-19.sparql](../sparql/cec2.md#cq-ce-5-19)

---