# In your admin_routes.py or app.py
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/api/subjects', methods=['GET'])
@jwt_required()
def get_all_subjects():
    cache_key = 'all_subjects'
    cached_subjects = redis_client.get(cache_key)

    if cached_subjects:
        return jsonify(json.loads(cached_subjects))
    else:
        subjects = Subject.query.all()
        subjects_data = [{'id': s.id, 'name': s.name, 'description': s.description} for s in subjects]
        # Cache for 1 hour (3600 seconds)
        redis_client.setex(cache_key, 3600, json.dumps(subjects_data))
        return jsonify(subjects_data)