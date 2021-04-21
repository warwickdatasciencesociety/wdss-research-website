using Agents
using Distributions
using StatsBase

mutable struct Sitter <: AbstractAgent
    id::Int
    eggs_laid::Int # How many eggs the agent lays
    egg_ids::Dict # Dictionary of the `id`s that have put an egg in this nest and their counts
    utility::Float64
end

mutable struct Identifier <: AbstractAgent
    id::Int
    eggs_laid::Int # How many eggs the agent lays
    egg_ids::Dict # Dictionary of the `id`s that have put an egg in this nest and their counts
    p_identify::Float64 # Probability of correctly identifying own agents
    utility::Float64
end

mutable struct Cheater <: AbstractAgent
    id::Int
    eggs_laid::Int # How many eggs the agent lays
    egg_ids::Dict
    utility::Float64
end

# Move order: Cheaters, Identifiers, Sitters, Model

"""
    agent_step!(cheater::Cheater, model)
Cheaters lay their eggs in a random nest. Note: cheaters do not build nests.
"""
function agent_step!(cheater::Cheater, model)
    if random_agent_type(model, [Sitter, Identifier]) != -1 # Will return -1 if there are no nests
        for _ in 1:cheater.eggs_laid
            rand_agent_id = random_agent_type(model, [Sitter, Identifier]) # Choose a random nest (i.e. random sitter or identifier)
            increment_dict!(model[rand_agent_id].egg_ids, cheater.id)
        end
    end
end

"""
    agent_step!(identifier::Identifier, model)
Identifiers lay eggs in their own nest, then identify their eggs successfully (with a certain probability) and destroy the rest 
"""
function agent_step!(identifier::Identifier, model)
    p = identifier.p_identify
    id = identifier.id
    eggs_laid = identifier.eggs_laid
    
    # Replace the dictionary with only your own eggs if perfect identification, else randomly destroy eggs from other birds
    if p == 1.0
        identifier.egg_ids = Dict(id => eggs_laid)
    else
        identifier.egg_ids[id] = rand(Binomial(eggs_laid, p))
        for other_id in setdiff(keys(identifier.egg_ids), [id])
            identifier.egg_ids[other_id] =  rand(Binomial(identifier.egg_ids[other_id], 1 - p))
        end
    end
end

"""
    agent_step!(sitter::Sitter, model)
Sitters simply lay eggs in their own nest.
"""

function agent_step!(sitter::Sitter, model)
    sitter.egg_ids[sitter.id] = sitter.eggs_laid
end



"""
    initialise_agents!(model, num_sitters, num_identifiers, num_cheaters)
This function is called in the creation of a new model and can also be used to "reset" a model
so it doesn't need to be re-defined for repeated testing.
"""
function initialise_agents!(model, num_sitters, num_identifiers, num_cheaters)
    genocide!(model)
    id = 0
    for _ in 1:num_sitters
        id += 1
        sitter = Sitter(id, model.eggs_laid, Dict{Int,Int}(), 0)
        add_agent!(sitter, model)
    end
    for _ in 1:num_identifiers
        id += 1
        identifier = Identifier(id, model.eggs_laid, Dict{Int,Int}(), model.p_identify, 0)
        add_agent!(identifier, model)
    end
    for _ in 1:num_cheaters
        id += 1
        cheater = Cheater(id, model.eggs_laid, Dict{Int,Int}(), 0)
        add_agent!(cheater, model)
    end
end


"""
    reproduce!(agent_type, model)
Adds an agent of a certain type to the model using the model's predefined parameters.
"""
function reproduce!(agent_type, model)
    id = nextid(model)
    if agent_type == Cheater
        offspring = Cheater(id, model.eggs_laid, Dict{Int,Int}(), 0)
        model.cheaters_extinct = 0
    elseif agent_type == Identifier
        offspring = Identifier(id, model.eggs_laid, Dict{Int,Int}(), model.p_identify, 0)
        model.identifiers_extinct = 0
    else
        offspring = Sitter(id, model.eggs_laid, Dict{Int,Int}(), 0)
        model.sitters_extinct = 0
    end
    add_agent!(offspring, model)
end


"""
    get_total_utility(model, agent_type)
Calculates the utility for the specified type
"""
function get_total_utility(model, agent_type)
    agents = collect(values(model.agents))
    filter!(a -> a isa agent_type, agents)
    utilities = getfield.(agents, :utility)
    return sum(utilities)
end


"""
    model_step!(model)
Performs a single step of the model which does the following:
1. Calculate the utility of every bird based on the formula for its type.
2. Kill a certian percentage of the population.
3. Repopulate the population (to its previous value) with types weighted by each type's total utility.
"""
function model_step!(model)
    nonextinct_types = unique(typeof.(allagents(model)))

    # Aggregate all egg_ids of non-extinct types into an array of IDs 
    nest_id_array = [id for (id, agent) in model.agents if typeof(agent) in intersect([Sitter, Identifier], nonextinct_types)]
    hatched_egg_dict = Dict{Int64,Int64}()
    for nest_id in nest_id_array
        for (egg_id, tally) in model.agents[nest_id].egg_ids
            increment_dict!(hatched_egg_dict, egg_id, tally)
        end
    end

    # Calculate utility of each agent and then type
    for (key, agent) in model.agents
        agent.utility = model.hatch_utility * get(hatched_egg_dict, key, 0) +
            Int(!isa(agent, Cheater)) * -model.egg_cost * get(agent.egg_ids, key, 0) +
            Int(isa(agent, Identifier)) * -model.identify_cost
    end

    # utilities = [
    #     sum(
    #         agent.utility
    #         for
    #         (key, agent) in
    #         Dict(id => agent for (id, agent) in model.agents if agent isa agent_type)
    #     ) for agent_type in nonextinct_types
    # ]

    utilities = map(agent_type -> get_total_utility(model, agent_type), nonextinct_types)
    
    # Resample population weighted by utility
    total_agents = nagents(model)
    killed_agents = Int(ceil(total_agents / 1))
    
    for _ in 1:killed_agents
        kill_agent!(random_agent(model), model)
    end
    
    # genocide!(model) # Kill all current agents before next batch are created in order to keep total_agents the same
    
    n_offspring = countmap(Distributions.sample(nonextinct_types, Weights(utilities), killed_agents))
    for (agent_type, count) in n_offspring
        for _ in 1:n_offspring[agent_type]
            reproduce!(agent_type, model)
        end
    end
    
    # Mutate population
    if rand() < model.p_mutation
        kill_agent!(random_agent(model), model) # Kill a random member in order to keep number of agents the same
        reproduce!(rand([Sitter, Identifier, Cheater]), model) # Sample from all 3 types as NSS can be interior
    end
    
    for variable in [model.sitters_extinct, model.identifiers_extinct, model.cheaters_extinct]
        variable = 1
    end
end

"""
    evolutionary_model(kwargs...)
Creates a model and initialises agents using the following parameters:
* num_sitters/num_identifiers/num_cheaters: the number of each type to initialise the model with,
* hatch_utility: the utility given to an agent for each successful egg that hatches,
* egg_cost: the cost per egg of sitting on eggs in your own nest,
* eggs_laid: the number of eggs that each agent lays per step,
* identify cost: the cost for identifiers to identify their eggs each step,
* p_identify: the probability that the identifier will correctly identify its own egg or a foreign egg (per egg, not aggregate),
* p_mutation: the probability per step that an agent in the population will mutate to an agent of any type
"""
function evolutionary_model(;
        num_sitters=1,
        num_identifiers=1,
        num_cheaters=1,
        hatch_utility=5.0,
        egg_cost=2.0,
        eggs_laid=1,
        identify_cost=1.0,
        p_identify=1,
        p_mutation=0
    )
    
    # Create model
    model = ABM(
        Union{Cheater,Identifier,Sitter},
        scheduler=by_type(false, true),
        properties=Dict(
            :eggs_laid => eggs_laid,
            :hatch_utility => hatch_utility,
            :egg_cost => egg_cost,
            :identify_cost => identify_cost,
            :p_identify => p_identify, 
            :p_mutation => p_mutation,
            :sitters_extinct => 1,
            :identifiers_extinct => 1,
            :cheaters_extinct => 1,
        ),
        warn=false # For use with mixed-agent models, supresses type warning
    )
    
    # Add agents to model
    initialise_agents!(model, num_sitters, num_identifiers, num_cheaters)
    return model
end

