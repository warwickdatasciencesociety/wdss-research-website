using Agents

"""
    magangle(x1, y1, x2, y2)
Return the magnitude and angle of the line given by two points
"""
function magangle(x1, y1, x2, y2)
    c = (x2-x1) + (y2-y1)*im
    return abs(c), angle(c)
end

rescale(x) = (x .- minimum(x))./(maximum(x)-minimum(x))

"""
    random_agent_model(model, agent_types)
Return the id of a random agent from the model of a certain type/s or -1 if there are no agents of this type
"""
function random_agent_type(model, agent_types)
    subdict = Dict(id => agent for (id, agent) in model.agents if typeof(agent) in agent_types)
    try 
        model[rand(keys(subdict))].id
    catch
        -1
    end
end

"""
    increment_dict!(dict, key, by=1)
Modify a dictionary element by a specified amount or set it to this amount if the key isn't present in the dictionary.
"""
function increment_dict!(dict, key, by=1)
     if haskey(dict, key)
        dict[key] += by
    else
        dict[key] = by
    end
end